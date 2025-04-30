from transformers import T5ForConditionalGeneration, T5Tokenizer

# Carga el modelo y el tokenizer
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

# Texto que quieres resumir
text = "summarize: La bomba del agua se dañó hoy en la mañana, no tenemos agua en todo el edificio, por favor ayudar."

# Tokenizar y preparar entrada
inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True)

# Generar el resumen
summary_ids = model.generate(inputs.input_ids, max_length=50, min_length=5, length_penalty=5., num_beams=2)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)
