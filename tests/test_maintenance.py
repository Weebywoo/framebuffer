import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy
from PIL import Image

from framebuffer.assets.loaders.image_loader import ImageLoader
from framebuffer.assets.loaders.image_writer import ImageWriter
from framebuffer.assets.loaders.mesh_loader import MeshLoader
from framebuffer.pipeline.shaders.fragment_shader import fragment_shader
from framebuffer.rendering.frame import Frame
from framebuffer.rendering.render_vertex_buffer import render_vertex_buffer
from framebuffer.scene.entity import Entity
from framebuffer.scene.model import Model
from framebuffer.scene.scene import Scene


class MaintenanceTests(unittest.TestCase):
    def test_scene_queries_preserve_order_and_subclasses(self) -> None:
        class ChildEntity(Entity):
            pass

        first, second = ChildEntity(), ChildEntity()
        scene = Scene(entities=[Entity(), first, second])
        self.assertIs(scene.find_entity(ChildEntity), first)
        self.assertEqual(scene.find_entities(ChildEntity), [first, second])
        self.assertIsNone(Scene().find_entity(Entity))

    def test_model_load_preserves_subclass(self) -> None:
        class ChildModel(Model):
            pass

        with (
            patch.object(MeshLoader, "load", return_value=([], [])),
            patch.object(ImageLoader, "load", return_value=numpy.zeros((1, 1, 3), dtype=numpy.uint8)),
        ):
            self.assertIsInstance(ChildModel.load("mesh.obj", "texture.png"), ChildModel)

    def test_image_modes_and_non_square_sampling(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"

            for mode in ("L", "RGBA", "P"):
                Image.new(mode, (7, 3)).save(path)
                texture = ImageLoader.load(str(path))
                self.assertEqual(texture.shape, (3, 7, 3))
                self.assertEqual(texture.dtype, numpy.uint8)

        texture = numpy.arange(3 * 7 * 3, dtype=numpy.uint8).reshape(3, 7, 3)
        color = fragment_shader(numpy.array([0.0, 0.0, 0.9, 0.75, 0.0]), texture=texture)
        numpy.testing.assert_array_equal(color, texture[1, 5])
        self.assertTrue(numpy.shares_memory(color, texture))

    def test_obj_blank_lines_comments_and_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mesh.OBJ"
            path.write_text("\n# mesh\nv 0 0 0\nv 1 0 0\nv 0 1 0\nvt 0 0\nvn 0 0 1\nf 1/1/1 2/1/1 3/1/1\n")
            vertices, indices = MeshLoader.load(str(path))
            self.assertEqual(len(vertices), 3)
            self.assertEqual(indices, [0, 1, 2])

    def test_bmp_row_padding_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.bmp"

            for width in range(1, 5):
                pixels = [[(10, 20, 30)] * width, [(40, 50, 60)] * width]
                ImageWriter.write(str(path), pixels)

                with Image.open(path) as image:
                    numpy.testing.assert_array_equal(numpy.array(image), pixels)

                row_size = (width * 3 + 3) // 4 * 4
                self.assertEqual(path.stat().st_size, 54 + row_size * 2)

    def test_frame_reuses_buffers_until_resize(self) -> None:
        frame = Frame(numpy.array([12, 4], dtype=numpy.uint16))
        color, depth = frame.color_buffer, frame.depth_buffer
        frame.set_size(numpy.array([12, 4], dtype=numpy.uint16))
        self.assertIs(frame.color_buffer, color)
        self.assertIs(frame.depth_buffer, depth)
        frame.set_size(numpy.array([4, 12], dtype=numpy.uint16))
        self.assertEqual(frame.depth_buffer.shape, (12, 4))
        self.assertAlmostEqual(frame.aspect_ratio, 1 / 3)

    def test_compiled_pipeline_draws_and_rejects_hidden_geometry(self) -> None:
        vertices = numpy.zeros((3, 11))
        vertices[:, :4] = [[-0.8, 0.8, 0.3, 1.0], [0.8, 0.8, 0.3, 1.0], [-0.8, -0.8, 0.3, 1.0]]
        vertices[:, 4:6] = 0.5
        original = vertices.copy()
        frame = Frame(numpy.array([8, 8], dtype=numpy.uint16))
        identity = numpy.eye(4)
        arguments = dict(
            frame_size=frame.size,
            color_buffer=frame.color_buffer,
            depth_buffer=frame.depth_buffer,
            model_matrix=identity,
            view_matrix=identity,
            projection_matrix=identity,
        )
        indices = numpy.array([0, 1, 2], dtype=numpy.uint32)
        render_vertex_buffer(
            vertices.ravel(),
            indices,
            texture=numpy.full((3, 7, 3), 80, dtype=numpy.uint8),
            **arguments,
        )
        visible = numpy.isfinite(frame.depth_buffer)
        self.assertTrue(visible.any())
        numpy.testing.assert_allclose(frame.depth_buffer[visible], 0.3)
        numpy.testing.assert_array_equal(vertices, original)
        vertices[:, 2] = 0.7
        render_vertex_buffer(
            vertices.ravel(),
            indices,
            texture=numpy.full((3, 7, 3), 160, dtype=numpy.uint8),
            **arguments,
        )
        self.assertTrue((frame.color_buffer[visible] == 80).all())
        numpy.testing.assert_allclose(frame.depth_buffer[visible], 0.3)


if __name__ == "__main__":
    unittest.main()
