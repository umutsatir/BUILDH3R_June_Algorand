from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
print("dispenser address:", dispenser.address)

creator = algorand.account.random()
print("creator address:", creator.address)
#print(algorand.account.get_information(creator.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

#print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="BUILDH3R",
        unit_name="H3R",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
print("asset id:", asset_id)

receiver = algorand.account.random()
print("receiver address:", receiver.address)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver.address,
        amount=10_000_000
    )
)

group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver.address,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver.address,
        receiver=creator.address,
        amount=1_000_000
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver.address,
        asset_id=asset_id,
        amount=50
    )
)

group_txn.execute()

print("receiver account asset balance:", algorand.account.get_information(receiver.address)["assets"][0]["amount"])
print("creator account asset balance:", algorand.account.get_information(creator.address)["assets"][0]["amount"])

# print(algorand.account.get_information(receiver.address))

algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=creator.address,
        clawback_target=receiver.address,
        asset_id=asset_id,
        amount=20
    )
)

print("post clawback:")
print("receiver account asset balance:", algorand.account.get_information(receiver.address)["assets"][0]["amount"])
print("creator account asset balance:", algorand.account.get_information(creator.address)["assets"][0]["amount"])
