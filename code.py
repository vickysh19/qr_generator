"""Generate a QR code image from text or a URL."""

import argparse
from pathlib import Path

try:
    import qrcode
except ModuleNotFoundError as error:
    if error.name != "qrcode":
        raise
    raise SystemExit(
        "Missing dependency 'qrcode'. Install it for this Python interpreter with: "
        "python -m pip install -r requirements.txt"
    ) from error


def generate_qr(data: str, output_path: Path) -> None:
    """Create a QR code image containing data and save it to output_path."""
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=16,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    image.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a QR code image from text or a URL."
    )
    parser.add_argument(
        "data",
        nargs="?",
        help="Text or URL to encode (prompted for if omitted).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("qr_code.png"),
        help="Output image path (default: qr_code.png).",
    )
    args = parser.parse_args()

    data = args.data if args.data is not None else input("Text or URL to encode: ")
    if not data.strip():
        parser.error("text or URL cannot be empty")

    try:
        generate_qr(data, args.output)
    except OSError as error:
        parser.error(f"could not save QR code to {args.output}: {error}")

    print(f"QR code saved to {args.output}")


if __name__ == "__main__":
    main()