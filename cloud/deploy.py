from __future__ import annotations


def build_cloud_run_deploy_command(
    *,
    service: str,
    region: str,
    project: str,
    source: str,
    model_path: str = "models/gesture-cnn-baseline-s05-partial.keras",
    model_version: str = "cnn-s05-partial-v1",
    api_key_secret: str = "gesture-api-key",
    demo: bool = False,
) -> list[str]:
    command = [
        "gcloud",
        "run",
        "deploy",
        service,
        f"--project={project}",
        f"--region={region}",
        f"--source={source}",
        "--allow-unauthenticated",
        f"--set-env-vars=MODEL_PATH={model_path},MODEL_TYPE=cnn,MODEL_VERSION={model_version}",
        f"--set-secrets=GESTURE_API_KEY={api_key_secret}:latest",
        "--memory=2Gi",
        "--cpu=2",
    ]
    if demo:
        command.append("--min-instances=1")
    return command
