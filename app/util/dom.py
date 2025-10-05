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
    def build_element(tag: str, attributes: dict[str, str], dom_content: str | None = None) -> str:
        if dom_content is None:
            return f"<{tag} {DomUtil.build_attributes_from_dict(attributes)}/>"
        return f"<{tag} {DomUtil.build_attributes_from_dict(attributes)}>{dom_content}</{tag}>"

    @staticmethod
    def wrap_with_html(dom_content: str, reload_delay_s: int, auto_reload: bool) -> str:
        auto_reload_meta: str = DomUtil.build_element("meta", {"http-equiv": "refresh", "content": f"{reload_delay_s}"})
        head: str = DomUtil.build_element("head", {}, auto_reload_meta if auto_reload else None)
        body: str = DomUtil.build_element("body", {"style": "margin: 0"}, dom_content)
        return DomUtil.build_element("html", {}, f"{head}{body}")
