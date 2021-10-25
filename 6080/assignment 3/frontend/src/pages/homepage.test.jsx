import React from 'react'
import Adapter from 'enzyme-adapter-react-16'
import { shallow, configure } from 'enzyme'
import HomePage from '../pages/homePage'

configure({ adapter: new Adapter() })

describe('Test the Homepage', () => {
  const wrapper = shallow(<HomePage />)

  it('contains a button with the "Sign In"', () => {
    expect(wrapper.find('.logInButton').text()).toEqual('Log in')
  })

  it('contains a button with the "Register"', () => {
    expect(wrapper.find('.registerButton').text()).toEqual('Register')
  })
})
