import time
from typing import Generator

import numpy

from framebuffer.math.linalg import Matrix
from framebuffer.pipeline.data.shader_context import ShaderContext
from framebuffer.pipeline.shaders.shader_utils import create_model_matrix, create_projection_matrix, create_view_matrix
from framebuffer.rendering.renderer import Renderer
from framebuffer.scene.camera import Camera
from framebuffer.scene.model import Model
from framebuffer.scene.scene import Scene


class GameEngine:
    def __init__(self, scene: Scene) -> None:
        self._scene: Scene = scene
        self._renderer: Renderer = Renderer()

    # TODO [severity 3/5, effort 3/5]: Poll input once per frame; share it across components.
    def _apply_components(self, elapsed_time: float, dt: float) -> None:
        for model in self._scene.entities:
            for component in model.components:
                component.apply(model.transform, elapsed_time, dt)

    def _render_frame(self) -> None:
        camera: Camera | None = self._scene.find_entity(Camera)

        if camera is None:
            return

        models: list[Model] = self._scene.find_entities(Model)
        view_matrix: Matrix[numpy.float64] = create_view_matrix(
            camera_position=camera.transform.position,
            camera_rotation=camera.transform.rotation,
        )

        with self._renderer.frame() as frame:
            projection_matrix: Matrix[numpy.float64] = create_projection_matrix(
                aspect_ratio=frame.aspect_ratio,
                fov=camera.fov,
                clipping=camera.clipping,
            )

            for model in models:
                model_matrix: Matrix[numpy.float64] = create_model_matrix(
                    scale=model.transform.scale,
                    rotation=model.transform.rotation,
                    position=model.transform.position,
                )
                shader_context: ShaderContext = ShaderContext(
                    view_matrix=view_matrix,
                    projection_matrix=projection_matrix,
                    model_matrix=model_matrix,
                    frame=frame,
                    texture=model.texture,
                    clipping=camera.clipping,
                )

                self._renderer.draw(model.mesh.vertices, model.mesh.indices, ctx=shader_context)

    @staticmethod
    # TODO [severity 2/5, effort 1/5]: Validate the window size; use a deque and rolling sum.
    def _frame_timer(moving_window: int = 100) -> Generator[tuple[float, float, float]]:
        frame_times: list[float] = []
        start_time: float = time.perf_counter()

        while True:
            frame_start_time: float = time.perf_counter()

            if len(frame_times) > 0:
                yield frame_times[-1], sum(frame_times) / len(frame_times), time.perf_counter() - start_time

            else:
                yield -1, -1, 0

            if len(frame_times) == moving_window:
                frame_times.pop(0)

            frame_times.append(time.perf_counter() - frame_start_time)

    # TODO [severity 2/5, effort 1/5]: Throttle and batch FPS overlay output.
    def _render_ui(self, last_frame_time: float, avg_frame_time: float, elapsed_time: float) -> None:
        print(f"\033[1;1HLAST FPS  {1 / last_frame_time:>3.0f} fps")
        print(f"\033[2;1HAVERAGE   {1 / avg_frame_time:>3.0f} fps")
        print(f"\033[3;1HLAST TIME {last_frame_time * 1000:>3.0f} ms")
        print(f"\033[4;1HAVERAGE   {avg_frame_time * 1000:>3.0f} ms")
        print(f"\033[5;1HELAPSED   {elapsed_time:>10.2f} s")
        print(f"\033[6;1HRESOLUTION {'x'.join(map(str, self._renderer.screen_size)):>9} px")

    # TODO [severity 4/5, effort 2/5]: Define first-frame dt and apply it consistently to motion components.
    def run(self) -> None:
        for last_frame_time, avg_frame_time, elapsed_time in self._frame_timer(moving_window=5):
            self._apply_components(elapsed_time, last_frame_time)
            self._render_frame()

            if last_frame_time and avg_frame_time:
                self._render_ui(last_frame_time, avg_frame_time, elapsed_time)
