#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contact Data Cleaner - Web App (Streamlit)
Converts PST files and Excel files to clean contact data
"""

import streamlit as st
import pandas as pd
import os
import tempfile
import re
from pathlib import Path
import shutil
import subprocess
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses

# Page config
st.set_page_config(
    page_title="Contact Data Cleaner",
    page_icon="📧",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #27ae60;
        color: black;
        font-weight: bold;
        padding: 0.5rem;
        font-size: 1.1rem;
    }
    .upload-section {
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📧 Contact Data Cleaner")
st.markdown("**Excel & PST Converter** - Extract and clean contact data from your files")

# File upload
st.markdown("### 📁 Upload Your File")
uploaded_file = st.file_uploader(
    "Choose an Excel (.xlsx, .xls, .csv) or PST (.pst) file",
    type=['xlsx', 'xls', 'csv', 'pst'],
    help="Supported formats: Excel, CSV, and PST files"
)

if uploaded_file is not None:
    # Show file info
    file_details = {
        "Filename": uploaded_file.name,
        "File size": f"{uploaded_file.size / 1024:.2f} KB",
        "File type": uploaded_file.type
    }
    
    with st.expander("📄 File Details", expanded=True):
        for key, value in file_details.items():
            st.write(f"**{key}:** {value}")
    
    # Convert button
    if st.button("🚀 Start Conversion", type="primary"):
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Save uploaded file to temp
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            status_text.text("🔄 Processing file...")
            progress_bar.progress(10)
            
            # Detect file type
            file_ext = Path(uploaded_file.name).suffix.lower()
            
            if file_ext in ['.xlsx', '.xls', '.csv']:
                status_text.text("📊 Processing Excel file...")
                contacts = process_excel_file(tmp_path, file_ext, progress_bar, status_text)
            elif file_ext == '.pst':
                status_text.text("📧 Processing PST file...")
                contacts = process_pst_file(tmp_path, progress_bar, status_text)
            else:
                st.error("❌ Unsupported file type!")
                os.unlink(tmp_path)
                st.stop()
            
            # Remove duplicates
            progress_bar.progress(75)
            status_text.text("🔍 Removing duplicates...")
            
            unique_contacts = []
            seen_emails = set()
            
            for contact in contacts:
                email = contact.get('email', '').strip().lower()
                if email and email not in seen_emails:
                    seen_emails.add(email)
                    normalized = dict(contact)
                    normalized['email'] = email
                    unique_contacts.append(normalized)
            
            # Create DataFrame
            progress_bar.progress(90)
            status_text.text("📝 Creating output file...")
            
            if unique_contacts:
                df = pd.DataFrame(unique_contacts)
                
                # Create download
                progress_bar.progress(100)
                status_text.text("✅ Conversion completed!")
                
                # Success message
                st.success(f"🎉 Success! Found {len(unique_contacts)} unique contacts")
                
                # Download button
                output_filename = f"cleaned_{Path(uploaded_file.name).stem}.xlsx"
                
                # Convert to Excel in memory
                from io import BytesIO
                output = BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)
                
                st.download_button(
                    label="📥 Download Cleaned Contacts",
                    data=output,
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                # Show preview
                with st.expander("👀 Preview (First 10 rows)", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Show stats
                st.markdown("### 📊 Statistics")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Contacts", len(contacts))
                col2.metric("Unique Contacts", len(unique_contacts))
                col3.metric("Duplicates Removed", len(contacts) - len(unique_contacts))
                
            else:
                st.warning("⚠️ No contacts found in the file!")
            
            # Cleanup
            os.unlink(tmp_path)
            
        except Exception as e:
            st.error(f"❌ Error during conversion: {e}")
            import traceback
            with st.expander("🔍 Error Details"):
                st.code(traceback.format_exc())
            if 'tmp_path' in locals():
                os.unlink(tmp_path)

else:
    # Instructions
    st.info("👆 Upload a file to get started")
    
    st.markdown("### ℹ️ How It Works")
    st.markdown("""
    1. **Upload** your Excel or PST file
    2. **Convert** - Extract all contacts with names and emails
    3. **Download** - Get a clean Excel file with:
       - Full Name
       - First Name
       - Last Name
       - Email
       - Domain
    
    **Features:**
    - ✅ Automatic duplicate removal
    - ✅ Email validation
    - ✅ Domain extraction
    - ✅ Supports multiple file formats
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ | Contact Data Cleaner v2.0")


# Helper Functions

def process_excel_file(file_path, file_ext, progress_bar, status_text):
    """Process Excel or CSV file to extract contact data"""
    try:
        status_text.text("📖 Reading file...")
        
        # Read file
        if file_ext == '.csv':
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        progress_bar.progress(30)
        status_text.text(f"📊 Processing {len(df)} rows...")
        
        # Look for contact columns
        contact_columns = []
        for col in df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in ['sender', 'recipient', 'from', 'to', 'email', 'name', 'contact', 'cc', 'bcc']):
                contact_columns.append(col)
        
        if not contact_columns:
            contact_columns = list(df.columns)
        
        # Extract contacts
        all_contacts = []
        total_rows = len(df)
        
        for idx, row in df.iterrows():
            for col in contact_columns:
                cell_value = str(row[col])
                if cell_value and cell_value != 'nan' and cell_value != 'None':
                    extracted_contacts = extract_multiple_contacts(cell_value)
                    all_contacts.extend(extracted_contacts)
            
            # Update progress
            if idx % 10 == 0:
                progress = 30 + int((idx / total_rows) * 40)
                progress_bar.progress(progress)
        
        progress_bar.progress(70)
        status_text.text(f"✅ Found {len(all_contacts)} contacts")
        
        return all_contacts
        
    except Exception as e:
        st.error(f"Error processing Excel file: {e}")
        return []


def process_pst_file(file_path, progress_bar, status_text):
    """Process PST file to extract contact data"""
    try:
        status_text.text("📧 Converting PST file...")
        progress_bar.progress(20)
        
        # Try pypff first
        try:
            import pypff
            pst_file = pypff.file()
            pst_file.open(file_path)
            
            root_folder = pst_file.get_root_folder()
            excel_data = [['Sender', 'Recipients', 'Subject', 'Date', 'Folder']]
            excel_data = extract_messages_from_folder(root_folder, excel_data)
            
            pst_file.close()
            
        except ImportError:
            # Fallback to readpst
            status_text.text("📧 Using alternative PST reader...")
            excel_data = convert_pst_via_readpst(file_path)
        
        progress_bar.progress(50)
        status_text.text(f"📧 Extracted {len(excel_data)-1} messages")
        
        # Extract contacts from messages
        contacts = []
        for idx, row in enumerate(excel_data[1:]):  # Skip header
            # Extract from sender
            if row[0]:
                sender_contacts = extract_multiple_contacts(row[0])
                contacts.extend(sender_contacts)
            
            # Extract from recipients
            if row[1]:
                recipient_contacts = extract_multiple_contacts(row[1])
                contacts.extend(recipient_contacts)
            
            # Update progress
            if idx % 25 == 0:
                progress = 50 + int((idx / len(excel_data)) * 20)
                progress_bar.progress(progress)
        
        progress_bar.progress(70)
        status_text.text(f"✅ Found {len(contacts)} contacts")
        
        return contacts
        
    except Exception as e:
        st.error(f"Error processing PST file: {e}")
        return []


def extract_messages_from_folder(folder, excel_data):
    """Extract messages from PST folder recursively"""
    try:
        # Process messages
        if hasattr(folder, 'get_number_of_sub_messages'):
            for msg_index in range(folder.get_number_of_sub_messages()):
                try:
                    message = folder.get_sub_message(msg_index)
                    
                    # Get message details
                    sender = safe_call(message, 'get_sender_name') or ''
                    sender_email = safe_call(message, 'get_sender_email_address') or ''
                    
                    if sender and sender_email and is_valid_email(sender_email):
                        sender = f"{sender} <{sender_email}>"
                    elif sender_email and is_valid_email(sender_email):
                        sender = sender_email
                    
                    recipients = get_recipients_list(message)
                    subject = safe_call(message, 'get_subject') or ''
                    date = safe_call(message, 'get_delivery_time') or ''
                    folder_name = safe_call(folder, 'get_name') or ''
                    
                    excel_data.append([sender, recipients, subject, str(date), folder_name])
                    
                except Exception:
                    continue
        
        # Process subfolders
        if hasattr(folder, 'get_number_of_sub_folders'):
            for sub_index in range(folder.get_number_of_sub_folders()):
                subfolder = folder.get_sub_folder(sub_index)
                excel_data = extract_messages_from_folder(subfolder, excel_data)
        
        return excel_data
        
    except Exception:
        return excel_data


def convert_pst_via_readpst(pst_path):
    """Fallback: use readpst CLI to convert PST"""
    try:
        readpst_path = shutil.which('readpst')
        if not readpst_path:
            st.warning("⚠️ readpst not found. Install via: brew install libpst (Mac) or apt-get install pst-utils (Linux)")
            return []
        
        temp_dir = tempfile.mkdtemp(prefix="pst_eml_")
        
        try:
            # Run readpst
            cmd = [readpst_path, '-e', '-o', temp_dir, '-q', pst_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                st.error(f"readpst failed: {result.stderr}")
                return []
            
            # Parse EML files
            excel_data = [['Sender', 'Recipients', 'Subject', 'Date', 'Folder']]
            
            for root, _, files in os.walk(temp_dir):
                folder_name = os.path.basename(root)
                for fname in files:
                    if fname.lower().endswith('.eml'):
                        fpath = os.path.join(root, fname)
                        try:
                            with open(fpath, 'rb') as f:
                                msg = BytesParser(policy=policy.default).parse(f)
                            
                            sender = msg.get('From', '')
                            recipients = ", ".join(filter(None, [msg.get('To', ''), msg.get('Cc', ''), msg.get('Bcc', '')]))
                            subject = msg.get('Subject', '')
                            date = msg.get('Date', '')
                            
                            excel_data.append([sender, recipients, subject, date, folder_name])
                        except Exception:
                            continue
            
            return excel_data
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception:
        return []


def extract_multiple_contacts(text):
    """Extract multiple contacts from comma-separated text"""
    contacts = []
    
    try:
        text = str(text).strip()
        if not text or text == 'nan' or text == 'None':
            return contacts
        
        # Split by commas
        contact_parts = [part.strip() for part in text.split(',')]
        
        for contact_part in contact_parts:
            if not contact_part:
                continue
            
            # Check for "Name <email>" format
            if '<' in contact_part and '>' in contact_part:
                email_start = contact_part.find('<')
                email_end = contact_part.find('>')
                if email_start != -1 and email_end != -1:
                    name_text = contact_part[:email_start].strip()
                    email = contact_part[email_start + 1:email_end].strip()
                    if name_text and email and is_valid_email(email):
                        contact = create_contact_from_name_email(name_text, email)
                        if contact:
                            contacts.append(contact)
            
            # Email only
            elif '@' in contact_part and '.' in contact_part:
                email = contact_part.strip()
                if is_valid_email(email):
                    contact = create_contact_from_email_only(email)
                    if contact:
                        contacts.append(contact)
        
        # Filter valid contacts
        valid_contacts = [c for c in contacts if c and 'email' in c and is_valid_email(c['email'])]
        return valid_contacts
        
    except Exception:
        return contacts


def create_contact_from_email_only(email):
    """Create contact object from email only"""
    try:
        username = email.split('@')[0]
        
        # Try to split username by common separators
        if '.' in username:
            parts = username.split('.')
            if len(parts) >= 2:
                first_name = parts[0].capitalize()
                last_name = parts[1].capitalize()
            else:
                first_name = username.capitalize()
                last_name = ''
        else:
            first_name = username.capitalize()
            last_name = ''
        
        contact = {
            'full_name': username.capitalize(),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'domain': extract_domain_from_email(email)
        }
        return contact
        
    except Exception:
        return None


def create_contact_from_name_email(name_text, email):
    """Create contact object from name and email"""
    try:
        # Clean name
        name_text = re.sub(r'[^\w\s]', ' ', name_text)
        name_text = re.sub(r'\s+', ' ', name_text).strip()
        
        if not name_text or len(name_text) < 2:
            return None
        
        # Split into first and last name
        name_parts = name_text.split()
        
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
        else:
            first_name = name_text
            last_name = ''
        
        contact = {
            'full_name': name_text,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'domain': extract_domain_from_email(email)
        }
        return contact
        
    except Exception:
        return None


def extract_domain_from_email(email):
    """Extract domain from email address"""
    if pd.isna(email) or not email or '@' not in str(email):
        return None
    try:
        domain = str(email).split('@')[1].strip()
        return domain
    except:
        return None


def is_valid_email(email):
    """Check if email is valid"""
    try:
        if not isinstance(email, str):
            return False
        email = email.strip()
        if not email or email.startswith('/'):
            return False
        if '@' not in email or '.' not in email:
            return False
        upper = email.upper()
        if any(p in upper for p in ['/O=', '/OU=', '/CN=', 'MIDBOROMGMNT', 'FIRST ADMINISTRATIVE GROUP', 'RECIPIENTS']):
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        username, domain = parts
        if not username or not domain or '.' not in domain:
            return False
        return True
    except Exception:
        return False


def safe_call(obj, method_name):
    """Safely call a method by name on an object"""
    try:
        method = getattr(obj, method_name, None)
        if callable(method):
            return method()
        return None
    except Exception:
        return None


def get_recipients_list(message):
    """Get recipients list as comma-separated string"""
    try:
        recipient_strings = []
        if hasattr(message, 'get_number_of_recipients'):
            for i in range(message.get_number_of_recipients()):
                try:
                    recipient = message.get_recipient(i)
                    name = safe_call(recipient, 'get_name') or ''
                    email_addr = safe_call(recipient, 'get_email_address') or ''
                    
                    if email_addr and name:
                        recipient_strings.append(f"{name} <{email_addr}>")
                    elif email_addr:
                        recipient_strings.append(email_addr)
                    elif name:
                        recipient_strings.append(name)
                except Exception:
                    continue
        
        return ", ".join([s for s in recipient_strings if s])
    except Exception:
        return ""

