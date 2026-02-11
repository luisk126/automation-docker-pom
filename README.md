## CI/CD

Este proyecto usa GitHub Actions para:

- Construir la imagen Docker
- Ejecutar pruebas Selenium
- Publicar la imagen en DockerHub

### Ejecutar local
docker run --rm -v ${PWD}:/workspace luiscadocker88/paquetes-automatizacion-gen pytest
