from cloud.deploy import build_cloud_run_deploy_command


def test_cloud_run_deploy_command_uses_min_instances_for_demo():
    command = build_cloud_run_deploy_command(
        service="gesture-api",
        region="asia-southeast1",
        project="iot-demo",
        source=".",
        demo=True,
    )

    assert "--min-instances=1" in command
    assert "--region=asia-southeast1" in command
    assert "--source=." in command
    assert "--memory=2Gi" in command
    assert "--cpu=2" in command
    assert "--set-secrets=GESTURE_API_KEY=gesture-api-key:latest" in command
