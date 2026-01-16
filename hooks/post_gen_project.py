import subprocess
import shutil
import os


def configure_dvc():
    """Configures DVC."""
    dataset_storage = "{{ cookiecutter.dataset_storage }}"
    
    try:
        # Initialize DVC if not already initialized
        if not os.path.exists(".dvc"):
             subprocess.run(["dvc", "init"], check=True)

        if dataset_storage == "s3":
            bucket = "{{ cookiecutter.s3_bucket_name }}"
            endpoint = "{{ cookiecutter.s3_endpoint_url }}"
            profile = "{{ cookiecutter.aws_profile }}"
            
            print(f"Configuring DVC for S3 bucket: {bucket}")
            
            # Add remote
            subprocess.run(["dvc", "remote", "add", "-d", "storage", f"s3://{bucket}"], check=True)
            
            # Set endpoint if provided (for self-hosted/minio)
            if endpoint:
                subprocess.run(["dvc", "remote", "modify", "storage", "endpointurl", endpoint], check=True)
            
            # Set profile if provided
            if profile and profile != "default":
                subprocess.run(["dvc", "remote", "modify", "storage", "profile", profile], check=True)
                
            print("DVC configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to configure DVC: {e}")
    except FileNotFoundError:
         print("dvc command not found. Skipping DVC configuration.")

def run_pre_commit_update():
    """Runs 'pre-commit autoupdate' if pre-commit is installed."""
    if shutil.which("pre-commit"):
        print("Running pre-commit autoupdate...")
        try:
            subprocess.run(["pre-commit", "autoupdate"], check=True)
            print("pre-commit hooks updated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to update pre-commit hooks: {e}")
    else:
        print("pre-commit not found. Skipping hook update.")


def init_git():
    """Initializes git configuration."""
    print("Initializing git repository...")
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit from cookiecutter template"], check=True)
        print("Git repository initialized.")
        print("\nTo push to GitHub, run:")
        print("  git remote add origin https://github.com/{{cookiecutter.github_owner}}/{{cookiecutter.repo_name}}.git")
        print("  git branch -M main")
        print("  git push -u origin main")
    except subprocess.CalledProcessError as e:
        print(f"Failed to initialize git: {e}")
    except FileNotFoundError:
        print("git command not found. Skipping git initialization.")

if __name__ == "__main__":
    init_git()
    configure_dvc()
    run_pre_commit_update()
