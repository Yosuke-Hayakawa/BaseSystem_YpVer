import logging
import io
import os
import base64
from pathlib import Path
from PIL import Image as PILImage
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

# 監査ログ設定（環境変数またはデフォルトパス）
_log_path = os.environ.get(
	"MCP_AUDIT_LOG",
	str(Path(__file__).resolve().parent / "mcp_audit.log")
)
logging.basicConfig(
	filename=_log_path,
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(message)s"
)

mcp = FastMCP("screenshot-server")

ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".bmp"}
MAX_BYTES = 10 * 1024 * 1024  # 10MB
MAX_DIMENSION = 7500  # API上限8000pxに余裕を持たせる
PNG_MAGIC = b"\x89PNG"
JPG_MAGIC = b"\xff\xd8\xff"
BMP_MAGIC = b"BM"

def _validate(path_str: str) -> Path:
	"""パス検証。違反は即例外"""
	p = Path(path_str).resolve()
	# シンボリックリンク禁止
	if p.is_symlink():
		raise PermissionError(f"シンボリックリンク拒否: {p}")
	# 拡張子チェック
	if p.suffix.lower() not in ALLOWED_EXT:
		raise ValueError(f"許可されない拡張子: {p.suffix}")
	# 存在チェック
	if not p.is_file():
		raise FileNotFoundError(f"ファイルなし: {p}")
	# サイズチェック
	if p.stat().st_size > MAX_BYTES:
		raise ValueError(f"サイズ超過: {p.stat().st_size / 1024 / 1024:.1f}MB")
	# マジックバイト確認（拡張子偽装対策）
	with open(p, "rb") as f:
		header = f.read(4)
	if not (header.startswith(PNG_MAGIC) or header.startswith(JPG_MAGIC) or header.startswith(BMP_MAGIC)):
		raise ValueError(f"ファイルヘッダが画像形式と一致しない: {p}")
	return p


def _resize_if_needed(p: Path) -> Image:
	"""画像がMAX_DIMENSIONを超えていたら縮小してbase64で返す"""
	img = PILImage.open(p)
	w, h = img.size
	if w <= MAX_DIMENSION and h <= MAX_DIMENSION:
		img.close()
		return Image(path=str(p))
	# アスペクト比を維持して縮小
	scale = min(MAX_DIMENSION / w, MAX_DIMENSION / h)
	new_w = int(w * scale)
	new_h = int(h * scale)
	img = img.resize((new_w, new_h), PILImage.LANCZOS)
	logging.info(f"リサイズ: {w}x{h} -> {new_w}x{new_h} path={p}")
	# base64で返す
	buf = io.BytesIO()
	fmt = "PNG" if p.suffix.lower() == ".png" else "JPEG"
	img.save(buf, format=fmt)
	img.close()
	return Image(data=base64.b64encode(buf.getvalue()).decode(), media_type=f"image/{fmt.lower()}")


@mcp.tool()
def view_image(path: str) -> Image:
	"""
	指定パスの画像をモデルに渡す。
	8000px超の画像は自動縮小。画像以外は拒否。
	"""
	try:
		p = _validate(path)
		logging.info(f"OK path={p}")
		return _resize_if_needed(p)
	except Exception as e:
		logging.warning(f"NG path={path} reason={e}")
		raise


@mcp.tool()
def list_images(folder: str) -> str:
	"""指定フォルダ内の画像一覧を返す"""
	d = Path(folder).resolve()
	if not d.is_dir():
		return f"フォルダが見つからない: {folder}"
	files = sorted(d.glob("*.png")) + sorted(d.glob("*.jpg")) + sorted(d.glob("*.jpeg")) + sorted(d.glob("*.bmp"))
	if not files:
		return "画像ファイルなし"
	return "\n".join(str(f) for f in files)


if __name__ == "__main__":
	mcp.run()