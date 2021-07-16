with import <nixpkgs> {};
let
  bibot_packages = python-packages: with python-packages; [
    pytest
    selenium
    beautifulsoup4

    pudb
    jedi
  ];
  bibot_python = python39.withPackages bibot_packages;
in
mkShell {
  nativeBuildInputs = [
    bibot_python
  ];
}
