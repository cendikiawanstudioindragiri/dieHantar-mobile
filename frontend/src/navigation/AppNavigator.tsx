import React from 'react';
import { NavigationContainer } from '@react-navigation/native';

export default function AppNavigator({ children }: any) {
  return <NavigationContainer>{children}</NavigationContainer>;
}
