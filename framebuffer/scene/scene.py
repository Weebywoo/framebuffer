from dataclasses import dataclass, field

from framebuffer.scene.entity import Entity


@dataclass
class Scene:
    entities: list[Entity] = field(default_factory=list)
    name: str = "default"

    # TODO [severity 3/5, effort 2/5]: Cache type queries; invalidate when entities change.
    def find_entities[EntityType: Entity](self, entity_type: type[EntityType]) -> list[EntityType]:
        return [entity for entity in self.entities if isinstance(entity, entity_type)]

    def find_entity[EntityType: Entity](self, entity_type: type[EntityType]) -> EntityType | None:
        return next((entity for entity in self.entities if isinstance(entity, entity_type)), None)
