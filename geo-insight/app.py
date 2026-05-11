import os
import sys
import traceback
import pandas as pd
from pathlib import Path

# Add src module to path
src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

print(f"[DEBUG] Current directory: {src_dir}")
print(f"[DEBUG] sys.path: {sys.path[:3]}")

import gradio as gr
from src.BriefingNoteWriter import brief_writer
from src.QueryInterpreter import interpret_query
from src.query_to_sql import filter_humanitarian_data
from src.query_to_articles import filter_articles

print("[DEBUG] All imports successful")

# Get path to CSV file
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
CSV_FILE_PATH = WORKSPACE_ROOT / "data" / "unocha_dataset.csv"
ARTICLES_FILE_PATH = WORKSPACE_ROOT / "data" / "reliefweb_dataset.csv"


print(f"[DEBUG] Workspace root: {WORKSPACE_ROOT}")
print(f"[DEBUG] CSV file path: {CSV_FILE_PATH}")
print(f"[DEBUG] CSV file exists: {CSV_FILE_PATH.exists()}")

# Main chat pipeline function
async def chat_pipeline(message, history):
    print(f"\n[DEBUG] === Starting chat_pipeline ===")
    print(f"[DEBUG] User message: {message}")
    print(f"[DEBUG] History length: {len(history)}")
    
    try:
        # Step 1: Agent 1 interprets the natural language query
        print("[DEBUG] Step 1: Calling interpret_query...")
        agent1_result = await interpret_query(message)
        agent_json = agent1_result.model_dump_json()
        print(f"[DEBUG] Agent 1 JSON: {agent_json}")

        # Step 2: Filter data from CSV
        print(f"[DEBUG] Step 2: Filtering data from CSV...")
        filtered_df = filter_humanitarian_data(agent_json, str(CSV_FILE_PATH))
        filtered_articles = filter_articles(agent_json, str(ARTICLES_FILE_PATH))
        
        print(f"[DEBUG] Filtered DataFrame shape: {filtered_df.shape}")
        print(f"[DEBUG] Filtered Articles shape: {filtered_articles.shape}")
        
        # If no results, try broader search
        if filtered_df.empty: 
            print("[DEBUG] No results found, trying broader search...")
            extended_user_message = message + " Check broader context like other countries in the area, similar context, or broader time period."
            agent1_extended_result = await interpret_query(extended_user_message)
            agent_json_extended = agent1_extended_result.model_dump_json()
            filtered_df_extended = filter_humanitarian_data(agent_json_extended, str(CSV_FILE_PATH))
            
            
            if filtered_df_extended.empty:
                return "The search did not find any matches in the Humanitarian Crises Database. Please try with different criteria."
            
            try:
                data_as_csv_string_extended = filtered_df_extended.to_csv(index=False)
                agent2_extended_result = await brief_writer(data_as_csv_string_extended, extended_user_message, "", agent1_extended_result.model_dump_json())
                df_markdown = "\n\n---\n\n## Data Table\n\n" + filtered_df_extended.to_markdown(index=False)
                return agent2_extended_result + df_markdown
            except Exception as brief_error:
                print(f"[DEBUG] Extended search briefing failed: {str(brief_error)}")
                return f"Found {len(filtered_df_extended)} records matching broader criteria:\n\n" + filtered_df_extended.to_markdown(index=False)
        
        # Step 3: Convert the filtered DataFrame to CSV
        print("[DEBUG] Step 3: Converting DataFrame to CSV...")
        data_as_csv_string = filtered_df.to_csv(index=False)
        articles_as_string = filtered_articles.to_csv(index=False) if not filtered_articles.empty else ""
        print(f"[DEBUG] CSV string length: {len(data_as_csv_string)} characters")

        # Step 4: Agent 2 generates the Briefing Note
        print("[DEBUG] Step 4: Calling brief_writer...")
        agent2_result = await brief_writer(data_as_csv_string, message, articles_as_string, agent1_result.model_dump_json())
        print(f"[DEBUG] Agent 2 result length: {len(agent2_result)} characters")
        
        # Append the filtered DataFrame as a markdown table
        print("[DEBUG] Appending filtered DataFrame to result...")
        # 1. Aggregation (Group by country)
        print_df = filtered_df.groupby("country_code").agg({
            "population": "max", 
            "total_required_funds": "sum", 
            "total_granted_funds": "sum", 
            "severity_index": "max" 
        }).reset_index()

        # Format columns
        print_df['population'] = print_df['population'].map(lambda x: f"{x/1000000:.1f}M" if pd.notnull(x) else "N/A")
        print_df['total_required_funds'] = print_df['total_required_funds'].map(lambda x: f"${x/1000000:.1f}M" if pd.notnull(x) else "N/A")
        print_df['total_granted_funds'] = print_df['total_granted_funds'].map(lambda x: f"${x/1000000:.1f}M" if pd.notnull(x) else "N/A")

        print_df = print_df.rename(columns={
            "country_code": "Country",
            "population": "Population",
            "total_required_funds": "Required Funds",
            "total_granted_funds": "Granted Funds",
            "severity_index": "Severity Index"
        })
        
        df_markdown = "\n\n---\n\n## Summary Data Table\n\n" + print_df.to_markdown(index=False)
        final_result = agent2_result + df_markdown
        
        print("[DEBUG] === Pipeline completed successfully ===\n")
        return final_result
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"[ERROR] Exception occurred: {str(e)}")
        print(f"[ERROR] Traceback:\n{error_traceback}")
        return f"**Pipeline Error:** {str(e)}"

print("[DEBUG] Configuring custom Gradio layout...")

# ==========================================
# CUSTOM UI STYLING & BEHAVIOR
# ==========================================

custom_css = """
/* Narrower container for better readability */
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
}

/* Force light background */
body, .gradio-container {
    background-color: #FDFBF7 !important;
}

/* Improve chat bubble styling for readability */
.message-wrap {
    font-size: 15px;
    line-height: 1.6;
}
.bot.message {
    background-color: #ffffff !important;
    border: 1px solid #eaeaea !important;
    color: #111111 !important;
    font-family: 'Times New Roman', Times, serif;
}
.user.message {
    background-color: #f3f4f6 !important;
    color: #111111 !important;
}

/* Fix Markdown Code / Inline Code Styling */
code, pre {
    background-color: #F5F5F5 !important;
    color: #111111 !important;
    border: 1px solid #E0E0E0 !important;
    border-radius: 4px !important;
}

/* Table Styling */
table {
    width: 100% !important;
    border-collapse: collapse !important;
    margin: 1em 0 !important;
}
table th, table td {
    border: 1px solid #DDDDDD !important;
    padding: 8px 12px !important;
    text-align: left !important;
}
table th {
    background-color: #F5F5F5 !important;
    font-weight: bold !important;
    color: #111111 !important;
}
"""

print("[DEBUG] Configuring Gradio interface...")

# Configure Gradio interface with enhanced styling
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    font=[gr.themes.GoogleFont("Helvetica Neue"), "ui-sans-serif", "system-ui", "sans-serif"],
).set(
    body_background_fill="#FDFBF7",
    color_accent_soft="#f3f4f6",
)

demo = gr.ChatInterface(
    fn=chat_pipeline,
    examples=[
        "Show underfunded food crises in the Sahel since 2022.",
        "Current humanitarian needs in Middle East.",
        "Countries with highest severity but lowest funding."
    ]
)

print("[DEBUG] Gradio interface configured")

if __name__ == "__main__":
    print("[DEBUG] Starting Gradio app launch...")
    with gr.Blocks(theme=theme, css=custom_css) as app:
        gr.Markdown("# Geo-Insight: Gap Finder Assistant\nAsk a natural language question about financial gaps in humanitarian crises. The system will query the underlying data and generate a professional briefing note.")
        demo.render()
        
    app.launch(share=True)
