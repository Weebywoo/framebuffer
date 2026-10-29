class ImageWriter:
    @classmethod
    def write(cls, filepath: str, data: list[list[tuple[int, int, int]]]) -> None:
        filename: str = filepath.split("/")[-1]

        match filename[filename.rfind(".") + 1 :]:
            case "bmp":
                cls.write_bmp(filepath, data)
                return

        raise ValueError(f"Unsupported file format: {filename}")

    @staticmethod
    def write_bmp(path: str, data: list[list[tuple[int, int, int]]]) -> None:
        # Each row in the Pixel array is padded to a multiple of 4 bytes in size
        image_data: list[bytes] = []

        for line in data:
            image_data_line: list[bytes] = []

            for pixel in line:
                image_data_line.append(int(pixel[2]).to_bytes())
                image_data_line.append(int(pixel[1]).to_bytes())
                image_data_line.append(int(pixel[0]).to_bytes())

            if (missing_padding := -len(image_data_line) % 4) != 0:
                image_data_line.append(bytes(missing_padding))

            image_data.extend(image_data_line)

        BITMAP_FILE_HEADER: dict[str, bytes] = {
            "bf_type": b"\x42\x4d",
            "bf_size": (14 + 40 + len(image_data)).to_bytes(4, "little"),
            "bf_reserved": b"\x00\x00\x00\x00",
            "bf_off_bits": b"\x36\x00\x00\x00",
        }
        BITMAP_INFO_HEADER: dict[str, bytes] = {
            "bi_size": b"\x28\x00\x00\x00",
            "bi_width": len(data[0]).to_bytes(4, "little"),
            "bi_height": (2**32 - len(data)).to_bytes(4, "little"),
            "bi_planes": b"\x01\x00",
            "bi_bit_count": b"\x18\x00",
            "bi_compression": b"\x00\x00\x00\x00",
            "bi_size_image": len(image_data).to_bytes(4, "little"),
            "bi_x_pels_per_meter": b"\x00\x00\x00\x00",
            "bi_y_pels_per_meter": b"\x00\x00\x00\x00",
            "bi_clr_used": b"\x00\x00\x00\x00",
            "bi_clr_important": b"\x00\x00\x00\x00",
        }

        with open(path, "wb") as file:
            file.write(b"".join(list(BITMAP_FILE_HEADER.values()) + list(BITMAP_INFO_HEADER.values()) + image_data))
