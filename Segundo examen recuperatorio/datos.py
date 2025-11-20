import os
import time
import shutil
from pathlib import Path

def iniciar_monitor():
    print("--- Monitor de Carpeta Compartida ---")
    
    target_ip = input("Introduce la IP objetivo (ej. 192.168.1.50): ").strip()
    resource = input("Introduce el nombre del recurso/carpeta (ej. Compartida): ").strip()

    source_path = Path(f"\\\\{target_ip}\\{resource}")
    dest_path = Path.home() / "Documents" / "data"
    
    try:
        dest_path.mkdir(parents=True, exist_ok=True)
        print(f"\n[OK] Carpeta de destino configurada en: {dest_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la carpeta local: {e}")
        return

    if not source_path.exists():
        print(f"[ERROR] No se puede acceder a {source_path}. Verifica la IP, el nombre del recurso o tus credenciales.")
        return

    print(f"[INFO] Escuchando en: {source_path}")
    print("[INFO] Presiona CTRL+C para detener el script.\n")

    try:
        while True:
            try:
                for item in source_path.glob('*'):
                    if item.is_file():
                        local_file = dest_path / item.name
                        if not local_file.exists():
                            print(f"[NUEVO] Detectado: {item.name}. Copiando...", end=" ")
                            try:
                                shutil.copy2(item, local_file)
                                print("¡Hecho!")
                            except PermissionError:
                                print("Error de permisos (el archivo podría estar en uso).")
                            except Exception as e:
                                print(f"Error al copiar: {e}")
            
            except OSError as e:
                print(f"[ADVERTENCIA] Perdida de conexión con la carpeta compartida: {e}")
                print("Reintentando en 5 segundos...")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[FIN] Monitor detenido por el usuario.")

if __name__ == "__main__":
    iniciar_monitor()