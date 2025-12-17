class FilenamePolicy:
    """Sanitizes strings for safe filenames."""

    def sanitize(self, name: str) -> str:
        """
        Replace problematic characters with underscores.

        Args:
            name: Original string

        Returns:
            Safe string for filenames
        """
        for c in '/\\:<>"|?*':
            name = name.replace(c, "_")
        return name
