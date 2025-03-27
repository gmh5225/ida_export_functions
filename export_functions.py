#!/usr/bin/env python3
"""
Export IDA Pro Function List to a Specified Path (Markdown Format)

Usage:
1. Open a binary file in IDA Pro
2. Go to File -> Script Command... or press Alt+F7
3. Select this script file
4. Choose the save location
5. Check the generated file

Export Format: Markdown table containing function addresses (hex) and names
"""

import os
import datetime
import idaapi
import idautils
import ida_funcs
import ida_name
import ida_kernwin
import ida_pro
import ida_nalt

def export_functions(output_path):
    """
    Export all function addresses and names to the specified Markdown file
    
    Args:
        output_path: Output file path
    
    Returns:
        Number of exported functions
    """
    count = 0
    
    try:
        with open(output_path, 'w', encoding='utf-8') as md_file:
            # Write file title
            binary_name = ida_nalt.get_root_filename()
            md_file.write(f"# Function List - {binary_name}\n\n")
            
            # Add export timestamp
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            md_file.write(f"Export Time: {current_time}\n\n")
            
            # Table headers
            md_file.write("| # | Address (Hex) | Address (Dec) | Function Name |\n")
            md_file.write("|------|--------------|------------|-------|\n")
            
            # Iterate through all functions
            for index, func_ea in enumerate(idautils.Functions(), 1):
                func_name = ida_name.get_name(func_ea)
                # Write function information
                md_file.write(f"| {index} | `0x{func_ea:X}` | {func_ea} | `{func_name}` |\n")
                count += 1
            
            # Add statistics
            md_file.write(f"\n\nTotal: {count} functions\n")
        
        print(f"Successfully exported {count} functions to: {output_path}")
        return count
    except Exception as e:
        print(f"Export failed: {str(e)}")
        return 0

def main():
    """Main function to get user input and execute the export"""
    
    # Get default save path (IDA database directory)
    try:
        default_dir = os.path.dirname(idaapi.get_input_file_path())
    except:
        default_dir = os.getcwd()
    
    default_filename = os.path.join(default_dir, "exported_functions.md")
    
    # Get user-specified output path
    output_path = ida_kernwin.ask_file(
        1,  # 1 means save file, 0 means open file
        "*.md",
        "Select path to save function list",
        default_filename
    )
    
    if not output_path:
        print("Export cancelled")
        return
    
    # Execute export
    count = export_functions(output_path)
    
    if count > 0:
        # Show success dialog
        ida_kernwin.info(f"Successfully exported {count} functions to:\n{output_path}")

if __name__ == "__main__":
    main()
