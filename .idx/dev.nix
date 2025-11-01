# To learn more about how to use Nix to configure your environment
# see: https://firebase.google.com/docs/studio/customize-workspace
{ pkgs, ... }: {
  # Which nixpkgs channel to use.
  channel = "stable-24.05"; # or "unstable"

  # Use https://search.nixos.org/packages to find packages for your environment.
  packages = [
    # Essential for Flutter development
    pkgs.flutter
    pkgs.dart
    # Required for the Android toolchain
    pkgs.jdk21
    pkgs.unzip
    # Firebase CLI for seamless integration
    pkgs.firebase-tools
  ];

  # Sets environment variables in the workspace.
  env = {
    # Set JAVA_HOME for the Android toolchain
    JAVA_HOME = "${pkgs.jdk21}";
  };

  # Firebase Studio-specific settings
  idx = {
    # VS Code extensions to install
    # Search for extensions on https://open-vsx.org/ and use "publisher.id"
    extensions = [
      "Dart-Code.flutter"
      "Dart-Code.dart-code"
    ];

    # Enable previews for hot reload
    previews = {
      enable = true;
    };

    # Commands to run on workspace startup
    workspace = {
      onStart = {
        # Install Flutter dependencies automatically
        get-deps = "flutter pub get";
      };
    };
  };
}
