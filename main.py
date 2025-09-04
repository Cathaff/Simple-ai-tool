from gmail_client import get_latest_email

from agent import analyze_email

 

def main():

    subject, body = get_latest_email()

    if subject is None:

        print("Inga mejl att läsa.")

        return

 

    print(f"Senaste mejlet:\nÄmne: {subject}\nInnehåll: {body[:200]}...\n")

 

    svar = analyze_email(subject, body)

    print("\n🤖 AI Agent svar:")

    print(svar)

 

if __name__ == "__main__":

    main()