# Name of the Python script
SCRIPT_NAME=main

# Output directory for the built executable
BUILD_DIR=dist

# PyInstaller options
PYINSTALLER_OPTS=--onefile --clean --name $(SCRIPT_NAME)

# Default target: build the executable
all: build

# Run PyInstaller to generate the executable
build:
	 PYTHONPATH=/usr/lib/python3/dist-packages pipx run pyinstaller $(PYINSTALLER_OPTS) $(SCRIPT_NAME).py

# Clean up build artifacts
clean:
	rm -rf build $(BUILD_DIR) $(SCRIPT_NAME).spec

# Run the built executable
run: build
	./$(BUILD_DIR)/$(SCRIPT_NAME)
