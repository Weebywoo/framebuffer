from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from framebuffer.scene.transform import Transform

if TYPE_CHECKING:
    from framebuffer.components.base_component import BaseComponent


@runtime_checkable
# TODO [severity 2/5, effort 2/5]: Review the unused runtime protocol and obsolete pipeline record types.
class _EntityProtocolRuntimeCheckable(Protocol):
    transform: Transform
    components: list[BaseComponent]


@dataclass
class Entity(_EntityProtocolRuntimeCheckable):
    transform: Transform = field(default_factory=Transform)
    components: list[BaseComponent] = field(default_factory=list)
