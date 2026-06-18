import os, shutil, zipfile
import torch

OUT = os.path.abspath("torch_test_02")
os.makedirs(OUT, exist_ok=True)

state = {
    "backbone.conv1.weight": torch.randn(16, 3, 3, 3),
    "backbone.conv1.bias":   torch.randn(16),
    "head.fc.weight":        torch.randn(10, 16),
    "head.fc.bias":          torch.randn(10),
}
ckpt_obj = {"state_dict": state, "epoch": 50, "global_step": 2000, "arch": "resnet-mini"}

def save_and_rename(saver, real_name, txt_name):
    real_path = os.path.join(OUT, real_name)
    saver(real_path)
    shutil.copyfile(real_path, os.path.join(OUT, txt_name))
    with open(real_path, "rb") as f:
        head = f.read(4)
    if head[:2] == b"PK":
        kind = "ZIP 容器(现代 torch)"
    elif head[:1] == b"\x80":
        kind = "裸 pickle(legacy)"
    else:
        kind = "其他"
    print(f"  {real_name:24s} 头={head.hex():10s} -> {kind}")

print("生成中...")
save_and_rename(lambda p: torch.save(state, p), "real_modern.pt",  "real_modern_pt.txt")
save_and_rename(lambda p: torch.save(state, p), "real_modern.pth", "real_modern_pth.txt")
save_and_rename(lambda p: torch.save(state, p, _use_new_zipfile_serialization=False),
                "real_legacy.pt", "real_legacy_pt.txt")
save_and_rename(lambda p: torch.save(ckpt_obj, p), "real_model.ckpt", "real_model_ckpt.txt")
save_and_rename(lambda p: torch.save(state, p), "pytorch_model.bin", "pytorch_model_bin.txt")

zip_path = os.path.join(OUT, "models_plain.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(OUT, "real_modern.pt"),  "real_modern.pt")
    z.write(os.path.join(OUT, "real_legacy.pt"),  "real_legacy.pt")
    z.write(os.path.join(OUT, "real_model.ckpt"), "real_model.ckpt")
print(f"  已生成普通压缩包: {os.path.basename(zip_path)}")

print(f"\n全部生成在: {OUT}")
print("加密压缩包请用 7-Zip / 归档工具设密码打包。")
