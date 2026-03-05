⚠ This project is still in early development and thus does not have any completed features yet. The README will be updated as the project progresses.

# Prencrypt
Prencrypt is an encryption tool which allows you to manually encrypt and decrypt messages. The public keys of all users
are stored on a central server for distribution. Private keys on the other hand are stored locally on the user's device.
Prencrypt uses the RSA algorithm for the exchange of AES-256 keys resulting in an E2E encryption model.

## Why all of this?
First and foremost this project is an educational experience for myself and maybe for you too. I was inspired to create
Prencrypt after the EU moved closer to implement their chat control act. Since I am a strong advocate for privacy and
security, I wanted to create a tool that allows users to communicate securely without facing on-device monitoring
by third parties.

## How does it work?
Prencrypt uses a combination of RSA and AES-256 encryption algorithms. When a user first connects to the network,
he is assigned a unique identifier and generates an RSA keypair which is then stored locally.
The server only stores the user's public key and unique identifier. When a user wants to exchange a secret AES key with
another party, he requests the recipient's public key from the server and uses it to encrypt the AES key.
The encrypted AES key is then sent to the recipient by the server. The recipient can then use his private RSA key to
decrypt the AES key and use it to encrypt and decrypt messages between the two parties.
Messages are encrypted using AES-256 in GCM mode, which provides both confidentiality and integrity.
The encrypted messages can then be sent through any communication channel, such as email or messaging apps,
without worrying about the security of the messages.

## Conclusion
Prencrypt is an educational project that demonstrates how to implement end-to-end encryption using RSA and 
AES-256 algorithms independently of any specific communication platform. It allows users to securely exchange messages
without relying on third-party services, making it a valuable tool for those who prioritize privacy and security in
their communications.

## Contributing
I would love to see people contribute to this project to make it better. If you have suggestions, improvements, or want
to help with development, please feel free to reach out or submit a pull request.