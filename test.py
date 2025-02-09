from PIL import Image
import os

def downscale_image(image: Image, scale: int) -> Image:
    width, height = image.size
    downscaled_image = image.resize((int(width / scale), int(height / scale)), Image.NEAREST)
    return downscaled_image


def resize_image(image: Image, size) -> Image:
    width, height = size
    resized_image = image.resize((width, height), Image.NEAREST)
    return resized_image

def limit_colors(
        image,
        limit: int=16,
        palette=None,
        palette_colors: int=256,
        quantize: Image.Quantize=Image.Quantize.MEDIANCUT,
        dither: Image.Dither=Image.Dither.NONE,
        use_k_means: bool=False
    ):
    if use_k_means:
        k_means_value = limit
    else:
        k_means_value = 0


    if palette:
        palette_image = palette
        ppalette = palette.getcolors()
        if ppalette:
            color_palette = palette.quantize(colors=len(list(set(ppalette))))
        else:
            colors = len(palette_image.getcolors()) if palette_image.getcolors() else palette_colors
            color_palette = palette_image.quantize(colors, kmeans=colors)
        #new_image = image.quantize(palette=color_palette, dither=dither)
    else:
        # we need to get palette from image, because
        # dither in quantize doesn't work without it
        # https://pillow.readthedocs.io/en/stable/_modules/PIL/Image.html#Image.quantize
        color_palette = image.quantize(colors=limit, kmeans=k_means_value, method=quantize, dither=Image.Dither.NONE)

    color_palette0 = image.quantize(colors=limit, kmeans=k_means_value, method=quantize, dither=Image.Dither.NONE)
    new_image = image.quantize(palette=color_palette0, dither=dither)
    image = new_image.convert("RGB")
    new_image = image.quantize(palette=color_palette, dither=dither)

    return new_image


if __name__ == "__main__":
    image_path = r"examples\00008-362389673.png" 
    original = Image.open(image_path)
    p_path = r"examples\482.152.png" 
    p_img = Image.open(p_path)


    image = downscale_image(original,8)
    palette = downscale_image(p_img,8)
    
    # Create output directory if it doesn't exist
    output_dir = "color_limit_tests"
    os.makedirs(output_dir, exist_ok=True)

    result = limit_colors(
                image,
                limit=16,
                palette=palette,
                palette_colors=256,
                #quantize=Image.Quantize.MEDIANCUT,
                quantize=Image.Quantize.MAXCOVERAGE,
                dither=Image.Dither.NONE,
                use_k_means=True,
            )
    result = resize_image(result,original.size)
    output_path = os.path.join(output_dir, "test.png")
    result.save(output_path)