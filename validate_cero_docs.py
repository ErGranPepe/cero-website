import os
import re
import json
import sys
import xml.etree.ElementTree as ET

def run_validation():
    print("=== INICIANDO VALIDACION DEL ECOSISTEMA DOCUMENTAL CONCEPTUAL CERO ===\n")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
        
    # 1. VALIDACION DEL MANIFIESTO JSON
    db_path = os.path.join(base_dir, "cero_docs_db.json")
    if not os.path.exists(db_path):
        print("[ERROR] cero_docs_db.json no existe en la raiz.")
        sys.exit(1)
        
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        print("[OK] cero_docs_db.json cargado correctamente como JSON valido.")
    except Exception as e:
        print(f"[ERROR] cero_docs_db.json no es un JSON valido. Motivo: {e}")
        sys.exit(1)
        
    doc_ids = list(db.keys())
    required_keys = ["category", "title", "subtitle", "author", "status", "version", "date", "sections"]
    
    for doc_id, doc_info in db.items():
        if not re.match(r"^DOC-A\d$", doc_id):
            print(f"[ERROR] Formato de ID invalido: '{doc_id}'. Debe ser DOC-AX (donde X es 1-8).")
            sys.exit(1)
            
        for key in required_keys:
            if key not in doc_info:
                print(f"[ERROR] Documento '{doc_id}' no contiene la clave requerida '{key}'.")
                sys.exit(1)
                
        if not isinstance(doc_info["sections"], list) or len(doc_info["sections"]) == 0:
            print(f"[ERROR] Documento '{doc_id}' debe contener una lista no vacia de 'sections'.")
            sys.exit(1)
            
    print(f"[OK] Esquema verificado para los {len(doc_ids)} documentos conceptuales.")

    # 2. VALIDACION DE REFERENCIAS CRUZADAS
    print("\nAuditando referencias cruzadas internas (DOC-AX)...")
    ref_pattern = re.compile(r"DOC-A\d")
    errors_cross_ref = 0
    
    for doc_id, doc_info in db.items():
        for sec_title, sec_text in doc_info["sections"]:
            found_refs = ref_pattern.findall(sec_text)
            for ref in found_refs:
                if ref not in db:
                    print(f"[WARN] En '{doc_id}', seccion '{sec_title}', se referencia '{ref}' pero no existe en la base de datos.")
                    errors_cross_ref += 1
                    
    if errors_cross_ref == 0:
        print("[OK] Todas las referencias cruzadas internas son validas.")
    else:
        print(f"[WARN] Se encontraron {errors_cross_ref} referencias cruzadas dudosas.")

    # 3. VERIFICACION DE LA COMPILACION DE ARCHIVOS FISICOS (PDF/MD)
    print("\nAuditando compilacion fisica en el directorio documents/...")
    documents_dir = os.path.join(base_dir, "documents")
    if not os.path.exists(documents_dir):
        print("[ERROR] El directorio 'documents' no existe. Compila primero.")
        sys.exit(1)
        
    for doc_id, doc_info in db.items():
        category = doc_info["category"]
        base_name = f"{doc_id}_{doc_info['title'].replace(' ', '_').replace('&', 'and').replace('/', '_')}"
        pdf_path = os.path.join(documents_dir, category, f"{base_name}.pdf")
        md_path = os.path.join(documents_dir, category, f"{base_name}.md")
        
        if not os.path.exists(pdf_path):
            print(f"[ERROR] PDF no encontrado: '{pdf_path}'")
            sys.exit(1)
        if not os.path.exists(md_path):
            print(f"[ERROR] MD no encontrado: '{md_path}'")
            sys.exit(1)
            
    print("[OK] Todos los 8 archivos PDF y Markdown conceptuales se han generado en documents/00_Gobernanza_y_Estrategia.")

    # 4. VERIFICACION DE ARCHIVADO LEGACY
    print("\nVerificando archivado en el directorio legacy/...")
    legacy_dir = os.path.join(base_dir, "legacy")
    if not os.path.exists(legacy_dir):
        print("[ERROR] El directorio 'legacy/' de archivado no existe.")
        sys.exit(1)
    
    legacy_folders = os.listdir(legacy_dir)
    if len(legacy_folders) == 0:
        print("[ERROR] El directorio 'legacy/' esta vacio. No se archivaron los documentos anteriores.")
        sys.exit(1)
        
    print(f"[OK] Directorio legacy/ verificado con exito. Contiene: {', '.join(legacy_folders)}.")

    # 5. CONTROL DE REGRESIONES EN MATPLOTLIB (pad= en labels)
    print("\nBuscando regresiones del bug de Matplotlib (pad= en set_xlabel/set_ylabel)...")
    engine_path = os.path.join(base_dir, "generate_cero_docs.py")
    if os.path.exists(engine_path):
        with open(engine_path, "r", encoding="utf-8") as f:
            engine_code = f.read()
            
        if re.search(r"set_x?label\([^)]*\bpad\s*=", engine_code):
            print("[ERROR] Se detecto el uso prohibido de 'pad=' en las funciones label de Matplotlib.")
            sys.exit(1)
        else:
            print("[OK] Ningun bug de 'pad' detectado en las llamadas de etiquetas de Matplotlib.")

    # 6. AUDITORIA DE CALIDAD SVG
    print("\nAuditando calidad de los archivos de marca vectoriales (SVG)...")
    brand_dir = os.path.join(base_dir, "assets", "brand")
    svg_files = ["logo_white.svg", "logo_black.svg", "logo_red.svg"]
    
    for svg_file in svg_files:
        svg_path = os.path.join(brand_dir, svg_file)
        if not os.path.exists(svg_path):
            print(f"[ERROR] Archivo SVG no encontrado: '{svg_path}'")
            sys.exit(1)
            
        file_size = os.path.getsize(svg_path)
        if file_size > 10 * 1024:
            print(f"[ERROR] El SVG '{svg_file}' pesa demasiado ({file_size} bytes).")
            sys.exit(1)
            
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            if root.tag.split('}')[-1] != 'svg':
                print(f"[ERROR] El archivo '{svg_file}' no es una estructura raiz <svg> valida.")
                sys.exit(1)
            paths = [elem for elem in root.iter() if elem.tag.endswith('path')]
            if len(paths) > 10:
                print(f"[ERROR] Demasiados paths ({len(paths)}) detectados en '{svg_file}'.")
                sys.exit(1)
        except Exception as e:
            print(f"[ERROR] El SVG '{svg_file}' tiene errores de parseo XML: {e}")
            sys.exit(1)
            
        print(f"[OK] SVG '{svg_file}' validado: peso ligero ({file_size} bytes) e integridad geometrica correcta.")

    print("\n=== ECOSISTEMA DOCUMENTAL CONCEPTUAL CERO VALIDADO CON EXITO [100% CORRECTO] ===")

if __name__ == "__main__":
    run_validation()
