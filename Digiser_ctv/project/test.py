package_name = "DA011223_PTPTVINH_KS1940_06"
# Split the package name by underscore
package_name_parts = package_name.split('_')

# Correct logic to create folder structure
if len(package_name_parts) >= 3:
    # Extract relevant parts
    ks_code = package_name_parts[2]  # KS1940
    folder1 = ks_code[:2]  # KS
    folder2 = ks_code[2:]  # 1940
    file_name = f"{package_name_parts[3]}.xlsx"  # 06.xlsx

    # Now you can use these to create the folder structure
    # KS -> 1940 -> 06.xlsx
    print(f"Folder Structure: {folder1}/{folder2}/{file_name}")
