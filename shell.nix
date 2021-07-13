with import <nixpkgs> {};
let
  bibot_packages = python-packages: with python-packages; [
    pytest
    selenium
  ];
  bibot_python = python3.withPackages bibot_packages;
in
mkShell {
  nativeBuildInputs = [
    bibot_python
  ];
}
