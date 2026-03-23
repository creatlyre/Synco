"""Generate PWA icons for Synco using pure Python (no Pillow dependency)."""

import struct
import zlib
import os


def create_png(width: int, height: int, bg_color: tuple, draw_calendar: bool = True, maskable: bool = False) -> bytes:
    """Create a simple PNG icon with brand color background and calendar symbol."""

    def make_pixel_row(y, w, h):
        row = bytearray()
        row.append(0)  # filter byte

        # For maskable icons, use center 80% as safe zone
        if maskable:
            padding = int(w * 0.1)
            cal_left = padding + int((w - 2 * padding) * 0.25)
            cal_right = w - padding - int((w - 2 * padding) * 0.25)
            cal_top = padding + int((h - 2 * padding) * 0.2)
            cal_bottom = h - padding - int((h - 2 * padding) * 0.2)
        else:
            cal_left = int(w * 0.25)
            cal_right = w - int(w * 0.25)
            cal_top = int(h * 0.2)
            cal_bottom = h - int(h * 0.2)

        cal_w = cal_right - cal_left
        border = max(2, w // 48)
        header_h = int((cal_bottom - cal_top) * 0.22)
        line_y = cal_top + header_h

        for x in range(w):
            in_cal = cal_left <= x <= cal_right and cal_top <= y <= cal_bottom

            if draw_calendar and in_cal:
                # Calendar pin posts (top)
                pin1_x = cal_left + int(cal_w * 0.3)
                pin2_x = cal_left + int(cal_w * 0.7)
                pin_top = cal_top - max(2, h // 32)
                is_pin = (abs(x - pin1_x) <= border or abs(x - pin2_x) <= border) and pin_top <= y <= cal_top + border

                # Calendar border
                is_border = (
                    (y <= cal_top + border) or
                    (y >= cal_bottom - border) or
                    (x <= cal_left + border) or
                    (x >= cal_right - border)
                )

                # Header area (darker)
                is_header = cal_top <= y <= line_y

                # Grid lines
                grid_area_top = line_y + border
                grid_area_h = cal_bottom - grid_area_top
                grid_area_w = cal_right - cal_left
                grid_rows = 4
                grid_cols = 5
                is_grid_line = False
                if y > line_y:
                    for r in range(1, grid_rows):
                        gy = grid_area_top + int(grid_area_h * r / grid_rows)
                        if abs(y - gy) <= max(1, border // 2):
                            is_grid_line = True
                    for c in range(1, grid_cols):
                        gx = cal_left + int(grid_area_w * c / grid_cols)
                        if abs(x - gx) <= max(1, border // 2):
                            is_grid_line = True

                if is_pin or is_border:
                    row.extend([255, 255, 255])  # white border/pins
                elif is_header:
                    row.extend([200, 200, 255])  # light blue header
                elif is_grid_line:
                    row.extend([180, 180, 220])  # light grid
                else:
                    row.extend([255, 255, 255])  # white body
            else:
                row.extend(bg_color)

        return bytes(row)

    # Build raw image data
    raw_data = b""
    for y in range(height):
        raw_data += make_pixel_row(y, width, height)

    # PNG file structure
    def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
        chunk = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(chunk) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + chunk + crc

    # PNG signature
    sig = b"\x89PNG\r\n\x1a\n"

    # IHDR
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
    ihdr = png_chunk(b"IHDR", ihdr_data)

    # IDAT
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b"IDAT", compressed)

    # IEND
    iend = png_chunk(b"IEND", b"")

    return sig + ihdr + idat + iend


def main():
    # Synco brand indigo
    bg = (99, 102, 241)  # #6366f1

    sizes = [192, 512]
    for size in sizes:
        # Regular icon
        data = create_png(size, size, bg, draw_calendar=True, maskable=False)
        path = f"public/icons/icon-{size}.png"
        with open(path, "wb") as f:
            f.write(data)
        print(f"Created {path} ({len(data)} bytes)")

        # Maskable icon (extra padding)
        data = create_png(size, size, bg, draw_calendar=True, maskable=True)
        path = f"public/icons/icon-maskable-{size}.png"
        with open(path, "wb") as f:
            f.write(data)
        print(f"Created {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
