"""Generate a cool D-pad style .ico file for AlwaysFnActive."""
from PIL import Image, ImageDraw
import os

def generate_icon():
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Background — rounded indigo square
        pad = max(1, size // 16)
        draw.rounded_rectangle(
            [pad, pad, size - pad, size - pad],
            radius=max(2, size // 6),
            fill=(99, 102, 241, 255),      # indigo
            outline=(139, 92, 246, 255),    # violet border
            width=max(1, size // 32)
        )

        cx, cy = size // 2, size // 2
        tri = max(3, size // 7)   # triangle size
        gap = max(4, size // 4)   # distance from center

        # Up arrow
        draw.polygon([
            (cx, cy - gap - tri),
            (cx - tri, cy - gap + 2),
            (cx + tri, cy - gap + 2),
        ], fill=(255, 255, 255, 255))

        # Down arrow
        draw.polygon([
            (cx, cy + gap + tri),
            (cx - tri, cy + gap - 2),
            (cx + tri, cy + gap - 2),
        ], fill=(255, 255, 255, 255))

        # Left arrow
        draw.polygon([
            (cx - gap - tri, cy),
            (cx - gap + 2, cy - tri),
            (cx - gap + 2, cy + tri),
        ], fill=(255, 255, 255, 255))

        # Right arrow
        draw.polygon([
            (cx + gap + tri, cy),
            (cx + gap - 2, cy - tri),
            (cx + gap - 2, cy + tri),
        ], fill=(255, 255, 255, 255))

        # Center glow dot
        dot_r = max(2, size // 14)
        draw.ellipse(
            [cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
            fill=(167, 139, 250, 255)  # violet glow
        )

        images.append(img)

    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    images[0].save(icon_path, format="ICO",
                   sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f"  Icon saved to: {icon_path}")

if __name__ == "__main__":
    generate_icon()
