from sentence_transformers import SentenceTransformer, util
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
class Resume:
  def __init__(self, ollama_server):
    self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    self.llm = Ollama(model='llama3.2',
                      base_url=ollama_server)

  def ats_score(self, resume_text: str, job_description: str) -> float:
    resume_embedding = self.embedder.encode(resume_text, 
                                            convert_to_tensor=True)
    job_description_embedding = self.embedder.encode(job_description, 
                                                     convert_to_tensor=True)
    similarity_score = util.pytorch_cos_sim(resume_embedding, 
                                            job_description_embedding).item()
    
    return round(similarity_score*100,2)
  
  def give_suggestions(self):
    feedback_prompt = PromptTemplate(
        input_variables=['resume', 'job'],
        template = '''
        You are an expert in resume Screnning

        Compare the Resume and Job Description:
        resume: {resume}

        Job Description Description: {job}

        - Check ATS Score (0-100)
        - Assign 3-5 actionable steps to improve the resume

        Respond in proper structured format.
        '''
    )

    feedback_chain = feedback_prompt | self.llm
    return feedback_chain
  
  def ats_system(self, resume: str, job: str):
    score = self.ats_score(resume, job)
    print(f"Resume: {resume} and job: {job}")
    feedback = self.give_suggestions().invoke({'resume': resume, 'job': job})
    print("suggesttions", feedback)
    return {'ats_score': score, 'feedback':feedback}