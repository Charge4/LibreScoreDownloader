import os
import subprocess
import shutil

# Paths
project_dir = r"C:\Users\Beso\Documents\Video_Downoader"
script_name = "Video_Downoader.py"
exe_name = "Video_Downoader.exe"
iss_file = "setup_script.iss"

# Step 1: Compile Python to .exe
print("🔧 ვამზადებთ .exe ფაილს PyInstaller-ით...")
subprocess.run([
    "pyinstaller",
    "--onefile",
    "--windowed",
    os.path.join(project_dir, script_name)
], check=True)

# Step 2: გადატანა dist-დან LibreScoreApp-ში
dist_path = os.path.join("dist", exe_name)
target_path = os.path.join(project_dir, exe_name)

if os.path.exists(target_path):
    os.remove(target_path)

shutil.move(dist_path, target_path)
print(f"✅ .exe ფაილი გადატანილია: {target_path}")

# Step 3: გაეშვას Inno Setup და შექმნას setup.exe
print("🚀 ვუშვებთ Inno Setup კომპილაციას...")

innosetup_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
iss_full_path = r"C:\Users\Beso\Documents\Video_Downoader\installer_script.iss"

subprocess.run([innosetup_path, iss_full_path], check=True)
print("🎉 ინსტალერი წარმატებით შეიქმნა!")
