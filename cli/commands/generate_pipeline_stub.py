from pathlib import Path
import typer
import yaml


ELK_TEMPLATE = """input {{
  beats {{
    port => 5044
  }}
}}
filter {{
  json {{ source => "message" }}
  mutate {{
    add_field => {{ "[@metadata][event_type]" => "%(event_type)s" }}
  }}
}}
output {{
  elasticsearch {{
    hosts => ["http://localhost:9200"]
    index => "finmon-%(event_type)s-%{{+YYYY.MM.dd}}"
  }}
}}
"""

LOKI_TEMPLATE = """clients:
  - url: http://localhost:3100/loki/api/v1/push
scrape_configs:
  - job_name: %(event_type)s
    static_configs:
      - targets: ['localhost']
        labels:
          event_type: %(event_type)s
          __path__: /var/log/*.log
"""


def _read_event_type(path: Path) -> str:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("event_type", "") or data.get("event_name", "event")


def generate_pipeline_stub(schema: Path, target: str, out: Path) -> None:
    event_type = _read_event_type(schema)
    template = ELK_TEMPLATE if target.lower() == "elk" else LOKI_TEMPLATE
    rendered = template % {"event_type": event_type}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(rendered, encoding="utf-8")
    typer.echo(f"Pipeline stub for {event_type} written to {out}")
