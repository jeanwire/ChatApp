import React, { useState, useCallback } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  if (!loggedIn) {
    return(
      <Login
        setLoggedIn={setLoggedIn}
      />
    )
  }
  return (
    <View style={styles.container}>
      <Text>Chats go here!</Text>
    </View>
  );
}

function Login(props) {
  const setLoggedIn = props.setLoggedIn;
  const [loginUsed, setLoginUsed] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // using a callback since we only want to make the API call on submission
  const validateInput = useCallback(() => {
    fetch('http://10.0.13.200:5000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
    .then(res => res.json())
    .then(res => handleResponse(res))
  }, [username, password]);

  const handleResponse = (response) => {
    console.log(response);
    if (response.status === 200) {
      setLoggedIn(true);
    }
    else {
      setLoginUsed(true);
    }
  };

  return (
    <View
      style={{...styles.container}}
    >
      {loginUsed &&
        <Text
          style={{color: 'red'}}
        >
          That username or password is incorrect.
        </Text>
      }
      <TextInput
      placeholder='Username'
      onChangeText={(text) => setUsername(text)}
      />
      <TextInput
      placeholder='Password'
      onChangeText={(text) => setPassword(text)}
      />
      <Button
        title={'Sign In'}
        onPress={() =>
          validateInput()
        }
      />
    </View>
  )

}

const styles = StyleSheet.create({
  container: {
    display: 'flex',
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
