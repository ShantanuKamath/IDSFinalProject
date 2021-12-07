#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy

app = hy.HydraApp(title='Secure Hydralit Data Explorer',favicon="💀",hide_streamlit_markers=False,use_navbar=True, navbar_sticky=True)
@app.addapp()
def my_home():
 hy.info('Hello from app1')

@app.addapp()
def app2():
 hy.info('Hello from app 2')


#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()