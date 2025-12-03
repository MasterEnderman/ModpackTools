from png_blender import TextureColorBlender
import os


def main():
    # Path to settings file
    settings_file = os.path.join(os.path.dirname(__file__), "settings.json")
    
    # Create blender instance and process all files
    blender = TextureColorBlender(settings_file)
    blender.process_all()


if __name__ == "__main__":
    main()
