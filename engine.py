import os
import json

# 1. Load the current game state
with open('state.json', 'r') as f:
    state = json.load(f)

# 2. Parse the move from the GitHub Issue title (Expected format: "ttt|4")
issue_title = os.environ.get('ISSUE_TITLE', '')
if not issue_title.startswith('ttt|'):
    print("Not a game move issue. Exiting.")
    exit(0)

try:
    move_index = int(issue_title.split('|')[1])
except:
    print("Invalid move format.")
    exit(0)

# 3. Update the board if the move is valid
if 0 <= move_index <= 8 and state['board'][move_index] == " ":
    state['board'][move_index] = state['turn']
    # Swap turn
    state['turn'] = "O" if state['turn'] == "X" else "X"

# 4. Save the new state
with open('state.json', 'w') as f:
    json.dump(state, f)

# 5. Generate the Markdown Board
# We use GitHub Issue URLs with pre-filled titles for the links
repo_url = "https://github.com/himesh-bhushan/himesh-bhushan/issues/new?title=ttt|"
markdown_board = "<table>\n"

for row in range(3):
    markdown_board += "  <tr>\n"
    for col in range(3):
        idx = row * 3 + col
        cell_val = state['board'][idx]
        
        if cell_val == " ":
            # Empty cell: Make it a clickable link to open an issue
            cell_content = f'<a href="{repo_url}{idx}">⬜</a>'
        elif cell_val == "X":
            cell_content = "❌"
        else:
            cell_content = "⭕"
            
        markdown_board += f'    <td align="center" width="50" height="50">{cell_content}</td>\n'
    markdown_board += "  </tr>\n"
markdown_board += "</table>\n"

# 6. Inject the board into the README template
with open('README.template.md', 'r') as f:
    template = f.read()

final_readme = template.replace('{board}', markdown_board)

with open('README.md', 'w') as f:
    f.write(final_readme)

print("Game engine execution complete!")
