# Function List (verify.py)
- "Verify or Hash or Quit? (v/h/q): "
  - If you press 'v', it'll use its existing registry of Hashes and verify if the files hashes are the same
    - If they are it'll say '<file> Is The Same'
    - If they aren't it'll say '<file> Has Been Tampered'
  - If you press 'h', it'll hash all the new bills and store the hashes (skipping existing ones)
  