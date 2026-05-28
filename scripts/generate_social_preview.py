import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_social_preview():
    # 2x supersampling dimensions
    width, height = 2560, 1280
    
    # 1. Base Image with clean off-white background
    img = Image.new('RGB', (width, height), '#FAFAFA')
    draw = ImageDraw.Draw(img)
    
    # Draw subtle developer grid (160x160px at 2x scale, representing 80x80px at 1x)
    grid_size = 160
    grid_color = '#F1F5F9'
    grid_width = 3
    for x in range(0, width, grid_size):
        draw.line([x, 0, x, height], fill=grid_color, width=grid_width)
    for y in range(0, height, grid_size):
        draw.line([0, y, width, y], fill=grid_color, width=grid_width)
        
    # Reinitialize draw object
    draw = ImageDraw.Draw(img)

    # Add a soft ambient gradient glow in the background to prevent it from being too flat
    def overlay_soft_glow(image, cx, cy, radius, color, max_opacity):
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        for r in range(radius, 0, -4):
            opacity = int(max_opacity * (1 - (r / radius)) ** 2)
            mask_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=opacity)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=40))
        color_layer = Image.new('RGB', (width, height), color)
        image.paste(color_layer, (0, 0), mask)

    # Soft, premium teal/green ambient glows on the corners matching "The Connector"
    overlay_soft_glow(img, 200, 200, 800, '#EBF5F0', 120)  # Soft green top-left
    overlay_soft_glow(img, 2360, 1080, 800, '#EFF6FF', 100) # Soft blue bottom-right
    
    # Reinitialize draw object after pasting glows
    draw = ImageDraw.Draw(img)

    # 2. Draw Left Column Elements
    x_offset = 160
    


    # --- CONDICIO LOGO MARK ("The Connector" SVG concept scaled to 2x) ---
    logo_cx, logo_cy = x_offset + 80, 440
    logo_r = 80
    
    # App Icon Background rounded rect - crisp white with boundary shadow
    draw.rounded_rectangle([logo_cx - logo_r - 2, logo_cy - logo_r - 2, logo_cx + logo_r + 2, logo_cy + logo_r + 2], radius=38, fill='#E2E8F0') # outer shadow layer
    draw.rounded_rectangle([logo_cx - logo_r, logo_cy - logo_r, logo_cx + logo_r, logo_cy + logo_r], radius=36, fill='#FFFFFF', outline='#CBD5E1', width=3)
    
    # Mathematical scaling of the SVG:
    # Original SVG viewBox is 0 0 200 200, width/height is 130px.
    # Inside the 160x160 app icon box (320x320px at 2x scale), we center the 130px logo (260px at 2x scale).
    # Scaling factor: 260 / 200 = 1.3!
    # Let's map coordinates:
    # Left-top of 260x260 logo box is centered inside 320x320 box.
    # Offset from logo_cx, logo_cy:
    # x_start = logo_cx - 130, y_start = logo_cy - 130.
    x_start = logo_cx - 130
    y_start = logo_cy - 130
    
    def scale_x(x):
        return x_start + x * 1.3
        
    def scale_y(y):
        return y_start + y * 1.3

    # Drawing the "The Connector" SVG components:
    # 1. Circular Arc 'C': d="M 148,48 A 70,70 0 1 0 148,152"
    # Center of circle is at SVG x=101.14, y=100. Radius=70.
    # Stroke thickness = 14 * 1.3 = 18.2 (use 18).
    arc_cx = scale_x(101.14)
    arc_cy = scale_y(100)
    arc_r_outer = 70 * 1.3 # 91
    arc_thickness = int(14 * 1.3) # 18
    
    # Pillow draw.arc bounding box
    # Angles: 48 degrees (bottom-right) to 312 degrees (top-right) in clockwise directions
    draw.arc([arc_cx - arc_r_outer, arc_cy - arc_r_outer, arc_cx + arc_r_outer, arc_cy + arc_r_outer], 48, 312, fill='#0F6E56', width=arc_thickness)
    
    # 2. Draw circular endcaps on the arc for smooth SVG stroke-linecap="round" behavior
    # Radius of circle center line: arc_r_mid = arc_r_outer - arc_thickness / 2 = 91 - 9 = 82
    arc_r_mid = arc_r_outer - arc_thickness / 2
    for angle in [48, 312]:
        rad = math.radians(angle)
        cap_x = arc_cx + arc_r_mid * math.cos(rad)
        cap_y = arc_cy + arc_r_mid * math.sin(rad)
        cap_r = arc_thickness / 2
        draw.ellipse([cap_x - cap_r, cap_y - cap_r, cap_x + cap_r, cap_y + cap_r], fill='#0F6E56')

    # 3. Horizontal Line 1: x1="148" y1="48" x2="177" y2="48" stroke-width="14"
    line1_y = scale_y(48)
    line1_x1 = scale_x(148)
    line1_x2 = scale_x(177)
    
    # Draw horizontal line 1
    draw.line([line1_x1, line1_y, line1_x2, line1_y], fill='#0F6E56', width=arc_thickness)
    # Draw rounded cap on the right side of the line
    draw.ellipse([line1_x2 - arc_thickness/2, line1_y - arc_thickness/2, line1_x2 + arc_thickness/2, line1_y + arc_thickness/2], fill='#0F6E56')

    # 4. Horizontal Line 2: x1="148" y1="152" x2="177" y2="152" stroke-width="14"
    line2_y = scale_y(152)
    line2_x1 = scale_x(148)
    line2_x2 = scale_x(177)
    
    # Draw horizontal line 2
    draw.line([line2_x1, line2_y, line2_x2, line2_y], fill='#0F6E56', width=arc_thickness)
    # Draw rounded cap on the right side of the line
    draw.ellipse([line2_x2 - arc_thickness/2, line2_y - arc_thickness/2, line2_x2 + arc_thickness/2, line2_y + arc_thickness/2], fill='#0F6E56')

    # 5. Three dots:
    # cx="173" r="4.5"
    # Dot 1: cy="90", opacity="0.3" -> Solid blended color on white background: #B7D4CC
    # Dot 2: cy="100", opacity="1.0" -> Solid #0F6E56
    # Dot 3: cy="110", opacity="0.3" -> Solid #B7D4CC
    dot_r = 4.5 * 1.3 # 5.85 (use 6)
    dot_cx = scale_x(173)
    
    draw.ellipse([dot_cx - dot_r, scale_y(90) - dot_r, dot_cx + dot_r, scale_y(90) + dot_r], fill='#B7D4CC')
    draw.ellipse([dot_cx - dot_r, scale_y(100) - dot_r, dot_cx + dot_r, scale_y(100) + dot_r], fill='#0F6E56')
    draw.ellipse([dot_cx - dot_r, scale_y(110) - dot_r, dot_cx + dot_r, scale_y(110) + dot_r], fill='#B7D4CC')

    # --- TITLE TEXT "Condicio" ---
    title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 128, index=1) # Helvetica Bold
    draw.text((x_offset + 200, 360), "Condicio", fill='#0F172A', font=title_font) # Deep charcoal for high contrast

    # --- MAIN SLOGAN / TEXT ---
    slogan_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 56, index=0) # Helvetica Regular
    draw.text((x_offset, 560), "Open standard for", fill='#334155', font=slogan_font)
    draw.text((x_offset, 640), "contract intelligence data", fill='#334155', font=slogan_font)

    # --- TAXONOMY PILLS (AT BOTTOM) ---
    tags = [
        ("parties", '#C7D2FE', '#EEF2FF', '#4F46E5'),
        ("clauses", '#BFDBFE', '#EFF6FF', '#1D4ED8'),
        ("obligations", '#A3D9C9', '#EBF5F0', '#0F6E56'), # Primary Teal for obligations (matching logo)
        ("risks", '#FBCFE8', '#FDF2F8', '#BE185D'),
        ("dates", '#FEF3C7', '#FFFBEB', '#B45309'),
        ("financials", '#A7F3D0', '#ECFDF5', '#047857')
    ]
    
    tag_x = x_offset
    tag_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 26, index=1)
    
    row1_tags = tags[:3]
    row2_tags = tags[3:]
    
    for tag_row, start_y in [(row1_tags, 860), (row2_tags, 950)]:
        curr_x = x_offset
        for label, border_c, bg_c, text_c in tag_row:
            text_bbox = draw.textbbox((0, 0), label, font=tag_font)
            text_w = text_bbox[2] - text_bbox[0]
            
            pill_w = text_w + 56
            pill_h = 60
            
            # Draw pill background and border
            draw.rounded_rectangle([curr_x, start_y, curr_x + pill_w, start_y + pill_h], radius=30, fill=bg_c, outline=border_c, width=3)
            # Draw pill text
            draw.text((curr_x + 28, start_y + 13), label, fill=text_c, font=tag_font)
            
            curr_x += pill_w + 24


    # 3. Draw Right Column Elements (JSON Schema Window)
    card_x1, card_y1 = 1520, 180
    card_x2, card_y2 = 2400, 1100
    
    # Shadow/Border glow behind the white window
    overlay_soft_glow(img, 1960, 640, 520, '#E2E8F0', 80)
    
    # Layer 1: Base rounded rect boundary shadow
    draw.rounded_rectangle([card_x1 - 4, card_y1 - 4, card_x2 + 4, card_y2 + 4], radius=44, fill='#F1F5F9')
    # Layer 2: White card background with outline
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=40, fill='#FFFFFF', outline='#E2E8F0', width=4)
    
    # macOS window controls
    control_y = card_y1 + 48
    dot_r = 10
    draw.ellipse([card_x1 + 48 - dot_r, control_y - dot_r, card_x1 + 48 + dot_r, control_y + dot_r], fill='#EF4444')
    draw.ellipse([card_x1 + 80 - dot_r, control_y - dot_r, card_x1 + 80 + dot_r, control_y + dot_r], fill='#F59E0B')
    draw.ellipse([card_x1 + 112 - dot_r, control_y - dot_r, card_x1 + 112 + dot_r, control_y + dot_r], fill='#10B981')
    
    # Tab title text
    tab_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22, index=1)
    draw.text((card_x1 + 160, control_y - 14), "schema/condicio.schema.json", fill='#94A3B8', font=tab_font)
    
    # Divider line under header
    draw.line([card_x1, card_y1 + 96, card_x2, card_y1 + 96], fill='#E2E8F0', width=3)
    
    # Code inner card background for distinct contrast block
    code_bg_x1, code_bg_y1 = card_x1 + 4, card_y1 + 98
    code_bg_x2, code_bg_y2 = card_x2 - 4, card_y2 - 4
    
    # Draw internal code panel background
    code_mask = Image.new('L', (width, height), 0)
    c_draw = ImageDraw.Draw(code_mask)
    c_draw.rounded_rectangle([code_bg_x1, code_bg_y1, code_bg_x2, code_bg_y2], radius=36, fill=255)
    code_panel_color = Image.new('RGB', (width, height), '#F8FAFC')
    img.paste(code_panel_color, (0, 0), code_mask)
    
    # Reinitialize draw
    draw = ImageDraw.Draw(img)
    
    # --- LIGHT THEME SYNTAX HIGHLIGHTED CODE SNIPPET ---
    # Primary brand colors utilized: Key=Teal(#0F6E56), Type/String=Emerald(#059669), Symbol/Brackets=Slate(#475569), SubKey=Violet(#7C3AED)
    code_lines = [
        ("{", [("{", '#475569')]),
        ("  \"$schema\": \"https://condicio.org/schema\",", [("  \"$schema\"", '#0F6E56'), (": ", '#475569'), ("\"https://condicio.org/schema\"", '#059669'), (",", '#475569')]),
        ("  \"type\": \"object\",", [("  \"type\"", '#0F6E56'), (": ", '#475569'), ("\"object\"", '#059669'), (",", '#475569')]),
        ("  \"required\": [", [("  \"required\"", '#0F6E56'), (": ", '#475569'), ("[", '#475569')]),
        ("    \"contract\", \"parties\", \"obligations\"", [("    \"contract\"", '#7C3AED'), (", ", '#475569'), ("\"parties\"", '#7C3AED'), (", ", '#475569'), ("\"obligations\"", '#7C3AED')]),
        ("  ],", [("  ]", '#475569'), (",", '#475569')]),
        ("  \"properties\": {", [("  \"properties\"", '#0F6E56'), (": ", '#475569'), ("{", '#475569')]),
        ("    \"contract\": { \"$ref\": \"#/defs/contract\" },", [("    \"contract\"", '#7C3AED'), (": ", '#475569'), ("{", '#475569'), (" \"$ref\"", '#0F6E56'), (": ", '#475569'), ("\"#/defs/contract\"", '#059669'), (" }", '#475569'), (",", '#475569')]),
        ("    \"parties\": {", [("    \"parties\"", '#7C3AED'), (": ", '#475569'), ("{", '#475569')]),
        ("      \"type\": \"array\",", [("      \"type\"", '#0F6E56'), (": ", '#475569'), ("\"array\"", '#059669'), (",", '#475569')]),
        ("      \"items\": { \"$ref\": \"#/defs/party\" }", [("      \"items\"", '#0F6E56'), (": ", '#475569'), ("{", '#475569'), (" \"$ref\"", '#0F6E56'), (": ", '#475569'), ("\"#/defs/party\"", '#059669'), (" }", '#475569')]),
        ("    },", [("    }", '#475569'), (",", '#475569')]),
        ("    \"obligations\": {", [("    \"obligations\"", '#7C3AED'), (": ", '#475569'), ("{", '#475569')]),
        ("      \"type\": \"array\",", [("      \"type\"", '#0F6E56'), (": ", '#475569'), ("\"array\"", '#059669'), (",", '#475569')]),
        ("      \"items\": { \"$ref\": \"#/defs/obligation\" }", [("      \"items\"", '#0F6E56'), (": ", '#475569'), ("{", '#475569'), (" \"$ref\"", '#0F6E56'), (": ", '#475569'), ("\"#/defs/obligation\"", '#059669'), (" }", '#475569')]),
        ("    }", [("    }", '#475569')]),
        ("  }", [("  }", '#475569')]),
        ("}", [("}", '#475569')])
    ]
    
    code_start_x = card_x1 + 64
    code_start_y = card_y1 + 140
    code_font = ImageFont.truetype('/System/Library/Fonts/SFNSMono.ttf', 30)
    line_height = 46
    
    # Draw syntax-colored tokens line by line
    for i, (line_text, tokens) in enumerate(code_lines):
        curr_y = code_start_y + (i * line_height)
        curr_x = code_start_x
        for token_text, token_color in tokens:
            draw.text((curr_x, curr_y), token_text, fill=token_color, font=code_font)
            bbox = draw.textbbox((0, 0), token_text, font=code_font)
            curr_x += bbox[2] - bbox[0]
            
    # 4. Resize with high-quality Lanczos scaling down to target 1280x640px
    target_width, target_height = 1280, 640
    final_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Create output directories if necessary
    os.makedirs('/Users/user/Projects/docfide/condicio/.github', exist_ok=True)
    
    # Save the output file
    final_img.save('/Users/user/Projects/docfide/condicio/.github/social-preview.png', 'PNG')
    print("Social preview image updated with 'The Connector' brand logo and theme!")

if __name__ == "__main__":
    create_social_preview()
