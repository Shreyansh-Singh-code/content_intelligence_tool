# bonus_ai_generator.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class AITweetGenerator:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_ai_tweet(self, prompt, max_length=60):
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=0.9,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        tweet = generated_text[len(prompt):].strip()
        
        # Clean up the tweet - remove URLs, mentions, and extra content
        # Stop at common delimiters
        for delimiter in ['\n', 'http', '@', '—', 'RT']:
            if delimiter in tweet:
                tweet = tweet[:tweet.index(delimiter)]
        
        # Remove incomplete sentences at the end
        tweet = tweet.strip()
        if tweet and not tweet[-1] in '.!?…':
            # Find last complete sentence
            for punct in ['.', '!', '?']:
                last_idx = tweet.rfind(punct)
                if last_idx > 0:
                    tweet = tweet[:last_idx + 1]
                    break
        
        return tweet[:280].strip()  # Twitter limit

# Add this to your API as a bonus endpoint