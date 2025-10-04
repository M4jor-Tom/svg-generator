class DomUtil:
    @staticmethod
    def escape_attribute(string: str) -> str:
        return (
            string.replace("&", "&amp;")
            .replace('"', "&quot;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    @staticmethod
    def build_attributes_from_dict(attributes: dict[str, str]) -> str:
        return " ".join(f'{key}="{DomUtil.escape_attribute(value)}"' for key, value in attributes.items())

    @staticmethod
    def build_str_color(rgb: tuple[float, float, float]) -> str:
        return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"

    @staticmethod
    def build_element(tag: str, attributes: dict[str, str]) -> str:
        return f"<{tag} {DomUtil.build_attributes_from_dict(attributes)}/>"

    @staticmethod
    def wrap_with_auto_reload_html(dom_content: str, reload_delay_s: int) -> str:
        return (f"<html>"
                f"<head><meta http-equiv='refresh' content='{reload_delay_s}' /></head>"
                f"{dom_content}"
                f"</html>")
