def rmsdCA_batch_auto(folder=".", puttyview="Y", bfactorca="CA"):
    # 引数の確認用のデバッグ出力
    print(f"[DEBUG] Folder: {folder}")
    print(f"[DEBUG] Puttyview: {puttyview}")
    print(f"[DEBUG] BfactorCA: {bfactorca}")
    
    folder = folder.strip('"').strip("'")
    results_dir = ensure_results_folder(folder)

    print(f"[INFO] Searching for PDBs in: {folder}")
    all_files = os.listdir(folder)
    
    # デバッグ: フォルダ内のファイルを確認
    print(f"[DEBUG] Files found: {all_files}")
    
    pdb_files = sorted([f for f in all_files if f.endswith(".pdb")])
    
    # デバッグ: pdbファイルのリストを確認
    print(f"[DEBUG] PDB files found: {pdb_files}")
    
    pdb_names = [os.path.splitext(f)[0] for f in pdb_files]
    pairs = [(pdb_names[i], pdb_names[j]) for i in range(len(pdb_names)) for j in range(i + 1, len(pdb_names))]
    print(f"[INFO] Total pairs to process: {len(pairs)}")

    summary_rows = [("Reference", "Target", "RMSD")]

    for i, (refMol, tgtMol) in enumerate(pairs, start=1):
        ref_path = os.path.join(folder, refMol + ".pdb")
        tgt_path = os.path.join(folder, tgtMol + ".pdb")

        print(f"\n[{i}/{len(pairs)}] Loading: {ref_path}, {tgt_path}")
        if not (os.path.exists(ref_path) and os.path.exists(tgt_path)):
            print(f"[WARNING] Missing file for: {refMol} or {tgtMol}")
            continue

        cmd.load(ref_path, refMol)
        cmd.load(tgt_path, tgtMol)
        cmd.refresh()

        print(f"[INFO] Running RMSD analysis on: {refMol} vs {tgtMol}")
        rmsd = rmsdCA(refMol, tgtMol, puttyview, bfactorca, results_dir)
        summary_rows.append((refMol, tgtMol, f"{rmsd:.3f}"))

        cmd.delete(refMol)
        cmd.delete(tgtMol)
        cmd.refresh()

    # CSV保存
    csv_path = os.path.join(results_dir, "rmsd_summary.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(summary_rows)

    print(f"\n[✔] Batch processing complete. Summary saved to: {csv_path}")
    # rmsdCA_batch_auto folder="E:/Ando/Documents/folder"