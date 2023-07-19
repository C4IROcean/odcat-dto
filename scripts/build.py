import os
import sys
from pathlib import Path
import json
import subprocess
from tempfile import TemporaryDirectory



def proto_files(source_dir: Path):
    for root, _, files in os.walk(source_dir.as_posix()):
        print("->", root, files)
        for fname in files:
            if fname.endswith(".proto"):
                yield Path(root) / fname


def build_protoc(source_dir: Path, build_dir: Path):
    import importlib_resources
    from grpc_tools import protoc

    well_known_protos_include = importlib_resources.files("grpc_tools") / "_proto"

    for proto_file in proto_files(source_dir):
        if proto_file.name == "options.proto":
            continue
        rel_path = proto_file.parent.relative_to(source_dir)
        jsonschema_out = build_dir / rel_path
        model_out = build_dir / rel_path / f"{proto_file.stem}_model.py"

        with TemporaryDirectory() as tmpdir:
            temp_dir_path = Path(tmpdir)
            command = [
                "grpc_tools.protoc",
                f"--proto_path={source_dir}",
                f"--proto_path={well_known_protos_include}",
                f"--jsonschema_out={temp_dir_path}",
                proto_file.as_posix(),
            ]
            if protoc.main(command) != 0:
                raise RuntimeError(f"error: {command} failed")

            created_file = list(temp_dir_path.iterdir())[0]
            jsonschema_file = jsonschema_out / f"{proto_file.stem}.schema.json"

            jsonschema_file.parent.mkdir(exist_ok=True, parents=True)
            jsonschema_file.open("w+").write(created_file.read_text())

            schema = json.load(jsonschema_file.open())
            if len(schema["definitions"]) > 1:
                model_out = model_out.parent

        print("Wrote JSONSchema to ", jsonschema_file)
        assert jsonschema_file.exists()

        subprocess.run(
            [
                sys.executable,
                "-m",
                "datamodel_code_generator",
                f"--input={jsonschema_file}",
                "--input-file-type=jsonschema",
                f"--output={model_out}",
                "--use-double-quotes",
                "--encoding=utf-8",
                "--reuse-model",
            ]
        )


def build(setup_kwargs):
    cwd = Path(__file__).parent.parent
    source_dir = cwd / "proto"
    build_dir = cwd

    build_dir.mkdir(exist_ok=True)

    build_protoc(source_dir, build_dir)


if __name__ == "__main__":
    build({})
