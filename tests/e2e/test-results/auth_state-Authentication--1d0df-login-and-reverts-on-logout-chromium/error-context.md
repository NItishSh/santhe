# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e3]:
    - generic [ref=e4]:
      - heading "Login" [level=3] [ref=e5]
      - paragraph [ref=e6]: Enter your email below to login to your account.
    - generic [ref=e7]:
      - generic [ref=e8]:
        - generic [ref=e9]:
          - generic [ref=e10]: Email
          - textbox "Email" [ref=e11]:
            - /placeholder: m@example.com
            - text: authtest-1769485286263@example.com
        - generic [ref=e12]:
          - generic [ref=e13]: Password
          - textbox "Password" [ref=e14]: Password123
      - generic [ref=e15]:
        - button "Sign in" [active] [ref=e16]
        - generic [ref=e17]:
          - text: Don't have an account?
          - link "Sign up" [ref=e18] [cursor=pointer]:
            - /url: /register
  - alert [ref=e19]
```