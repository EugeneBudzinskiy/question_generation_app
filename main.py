__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st


def main():
    pg = st.navigation(
        pages=[
            st.Page("home.py", title="Home", icon=":material/home:"),
            st.Page("quiz.py", title="Quiz", icon=":material/quiz:")
        ],
        position="hidden"
    )
    pg.run()


if __name__ == '__main__':
    main()
