import subprocess
import time

class DockerManager:
    @staticmethod
    def run_docker_compose():
        try:
            # Rodar o docker-compose para levantar os containers
            subprocess.run(["docker-compose", "-p", "citus", "up", "-d"], check=True)
            print("Docker containers are up and running.")
        except subprocess.CalledProcessError as e:
            print(f"Error running docker-compose: {e}")
        time.sleep(15)  # Esperar os containers subirem totalmente

    @staticmethod
    def stop_docker_compose():
        try:
            subprocess.run(["docker-compose", "-p", "citus", "down"], check=True)
            print("Docker containers have been stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping docker-compose: {e}")
