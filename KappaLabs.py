from flask import Flask, request, jsonify
import transformers 
import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_input(data):
  processed_data = {
      "Property_title": data.get("Property Title"),  
      "Location": data.get("Location"),
  }
  return processed_data

def generate_copy(processed_data):
  model = transformers.BartForConditionalGeneration.from_pretrained("facebook/bart-base")
  tokenizer = transformers.BartTokenizer.from_pretrained("facebook/bart-base")
  prompt = f"Write a compelling real estate marketing brochure for a {processed_data['Property_title']} property in {processed_data['Location']}"
  input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
  output = model.generate(
      input_ids=input_ids,
      max_length=512,  
      num_beams=5,  
      early_stopping=True,
      no_repeat_ngram_size=2,  
      temperature=0.7,  
      do_sample=True
  )

  generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
  return generated_text

app = Flask(__name__)
if __name__ == '__main__':
  app.run(debug=True)
  
@app.route('/generate-copy', methods=['POST'])
def generateCopyRoute():
  if request.method == 'POST':
    try:
      data = pd.read_csv(r'F:/Python Files/real_estate.csv') 
      processed_data = preprocess_input(data)
      copy = generate_copy(processed_data)
      return jsonify({'copy': copy})
    except Exception as e: 
      print(f"Error generating copy: {e}")
      return jsonify({'error': 'An error occurred. Please try again later.'}), 500


