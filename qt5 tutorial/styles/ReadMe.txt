Relocate the location of qt material theme xml

modify the following file "C:\Users\user\AppData\Roaming\Python\Python310\site-packages\qt_material\hook-qt_material.py"

Replace:
themes_path = qt_material_path / "themes"
datas += [(str(themes_path), "qt_material/themes")]


# Change the themes_path to your desired location
themes_path = Path(r"C:\Users\user\Documents\python\buttons\QuickNotes\styles")
datas += [(str(themes_path), "qt_material/themes")]
