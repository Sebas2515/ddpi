"""
Script principal para ejecutar el pipeline de procesamiento RMC.
Reportes Mensuales de Comercio - Automatización de datos comerciales.
"""

import logging
import sys
from pathlib import Path
from src.pipeline import run_pipeline

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Función principal que ejecuta el pipeline."""
    try:
        logger.info("\n" + "="*70)
        logger.info("INICIÓ EJECUCIÓN DEL PIPELINE RMC")
        logger.info("="*70 + "\n")
        
        run_pipeline()
        
        logger.info("\n" + "="*70)
        logger.info("✅ EJECUCIÓN COMPLETADA EXITOSAMENTE")
        logger.info("="*70 + "\n")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Pipeline interrumpido por el usuario")
        return 1
    except FileNotFoundError as e:
        logger.error(f"\n❌ ARCHIVO NO ENCONTRADO: {str(e)}")
        return 2
    except Exception as e:
        logger.error(f"\n❌ ERROR CRÍTICO: {str(e)}")
        logger.exception("Traceback completo:")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)