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
    def build_str_color(rgb_or_rgba: tuple[float, float, float] | tuple[float, float, float, float]) -> str:
        if len(rgb_or_rgba) == 4:
            return f"rgba({rgb_or_rgba[0]}, {rgb_or_rgba[1]}, {rgb_or_rgba[2]}, {rgb_or_rgba[3]})"
        return f"rgb({rgb_or_rgba[0]}, {rgb_or_rgba[1]}, {rgb_or_rgba[2]})"

    @staticmethod
    def build_element(tag: str, attributes: dict[str, str], dom_content: str | None = None) -> str:
        if dom_content is None:
            return f"<{tag} {DomUtil.build_attributes_from_dict(attributes)}/>"
        return f"<{tag} {DomUtil.build_attributes_from_dict(attributes)}>{dom_content}</{tag}>"

    @staticmethod
    def build_css_statement_from_dict(properties: dict[str, str]) -> str:
        return ';'.join([f"{key}: {value}" for key, value in properties.items()])

    @staticmethod
    def wrap_with_html(dom_content: str, background_rgb: tuple[float, float, float],
                       reload_delay_s: int | None = None) -> str:
        auto_reload: bool = reload_delay_s is not None
        auto_reload_meta: str = DomUtil.build_element("meta", {"http-equiv": "refresh", "content": f"{reload_delay_s}"})
        head: str = DomUtil.build_element("head", {}, auto_reload_meta if auto_reload else None)
        body: str = DomUtil.build_element("body", {"style": DomUtil.build_css_statement_from_dict({
            "margin": "0",
            "text-align": "center",
            "background-color": DomUtil.build_str_color(background_rgb)
        })}, dom_content)
        return DomUtil.build_element("html", {}, f"{head}{body}")
