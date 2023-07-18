import os
from pathlib import Path


def proto_files(source_dir: Path):
    for root, _, files in os.walk(source_dir.as_posix()):
        print("->", root, files)
        for fname in files:
            print("--->", fname)
            if fname.endswith(".proto"):
                yield Path(root) / fname


def build_protoc(source_dir: Path, build_dir: Path):
    from grpc_tools import protoc
    import importlib_resources

    well_known_protos_include = importlib_resources.files("grpc_tools") / "_proto"

    for proto_file in proto_files(source_dir):
        print("--->", proto_file)
        command = [
            "grpc_tools.protoc",
            f"--proto_path={source_dir}",
            f"--proto_path={well_known_protos_include}",
            f"--python_out={build_dir}",
            f"--pyi_out={build_dir}",
            f"--protobuf-to-pydantic_out={build_dir}",
            proto_file.as_posix(),
        ]
        if protoc.main(command) != 0:
            raise RuntimeError(f"error: {command} failed")


def build(setup_kwargs):
    cwd = Path(__file__).parent.parent
    source_dir = cwd / "proto"
    build_dir = cwd / "odp" / "dto"

    build_dir.mkdir(exist_ok=True)

    build_protoc(source_dir, build_dir)


if __name__ == "__main__":
    build({})

