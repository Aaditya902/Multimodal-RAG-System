ERRORS = {
    'no_api_key': "⚠️ Google API key not found. Please set GOOGLE_API_KEY in your .env file",
    'no_file': "⚠️ Please upload at least one file",
    'no_query': "⚠️ Please enter a question",
    'processing_failed': "❌ Error processing file: {error}",
    'ocr_failed': "❌ OCR failed: {error}",
    'gemini_failed': "❌ Gemini API error: {error}",
    'no_results': "No relevant information found in your documents.",
    'file_too_large': "❌ File too large. Max size: {max_size}MB",
    'unsupported_type': "❌ Unsupported file type: {file_type}",
}

SUCCESS = {
    'files_processed': "✅ Processed {count} files with {chunks} chunks",
    'file_uploaded': "✅ Uploaded: {filename}",
    'ocr_success': "✅ OCR completed for {count} images",
    'api_connected': "✅ Successfully connected to Gemini API",
}

INFO = {
    'welcome': "Upload any file - PDF, Images, Word, Excel - and ask questions!",
    'no_files': "👈 Upload files to start asking questions",
    'processing': "🔄 Processing {filename}...",
    'thinking': "🤔 Thinking with Gemini...",
    'searching': "🔍 Searching documents...",
}

PROMPTS = {
    'qa_system': """You are a helpful assistant that answers questions based on provided documents.

CONTEXT:
{context}

QUESTION: {query}

INSTRUCTIONS:
1. Answer ONLY using the provided context
2. If information is not in context, say "I cannot find this information in your documents"
3. Be concise and accurate
4. Mention which document the information comes from

ANSWER:""",

    'image_analysis': """Analyze this image comprehensively.

OCR text found: {ocr_text}

Please describe:
1. What is shown in this image?
2. If it's a diagram/chart, explain its meaning
3. Any important details or context
4. How does this relate to any text found?

DESCRIPTION:""",

    'summarize': """Summarize the following text:

{text}

Provide a concise summary covering the main points:

SUMMARY:""",
}

UI = {
    'app_title': "🔄 Multimodal RAG System with Gemini",
    'upload_header': "📁 File Upload",
    'process_button': "🚀 Process Files",
    'clear_button': "🗑️ Clear All",
    'ask_header': "💬 Ask Questions",
    'answer_header': "📝 Answer",
    'settings_header': "⚙️ Settings",
    'stats_header': "📊 Usage Statistics",
    'model_select': "Gemini Model",
    'threshold_slider': "Similarity Threshold",
    'max_results': "Max Results",
    'reset_stats': "🔄 Reset Stats",
}

HELP = {
    'threshold': "Lower = more results, Higher = stricter matching",
    'model': "Select which Gemini model to use",
    'ocr_calls': "Free local OCR calls",
    'vision_calls': "Gemini Vision API calls",
    'text_calls': "Gemini Text API calls",
}